import torch
from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image
from typing import List, Optional, Dict, Union
import logging
import requests
from io import BytesIO
import math
import os
from torch.utils.data import DataLoader
from tqdm.autonotebook import tqdm
import base64
from io import BytesIO
import requests
import dashscope
from http import HTTPStatus
import numpy as np




logger = logging.getLogger(__name__)

def custom_collate_fn(batch):
    """Custom batch processing function"""
    return batch



class GmeAPI:
    def __init__(self, api_key: str = None):
        """Initialize GME API client
        
        Args:
            api_key: DashScope API key
        """
        self.api_key = api_key
        if api_key:
            dashscope.api_key = api_key

    def _image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 format
        
        Args:
            image_path: Image path
            
        Returns:
            str: Base64 encoded image data
        """
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        image_format = image_path.split('.')[-1].lower()
        return f"data:image/{image_format};base64,{base64_image}"

    def get_embedding(self, text: str = None, image_path: str = None) -> np.ndarray:
        """Get multimodal embedding vector for text and image
        
        Args:
            text: Text content
            image_path: Image path
            
        Returns:
            np.ndarray: Generated embedding vector
        """
        # Prepare input data
        input_data = {'text': text} if text else {}
        if image_path:
            input_data['image'] = self._image_to_base64(image_path)
            
        inputs = [input_data]

        # Call GME API
        resp = dashscope.MultiModalEmbedding.call(
            model="multimodal-embedding-v1",
            input=inputs
        )
        
        if resp.status_code == HTTPStatus.OK:
            # Get embedding vector
            embedding = np.array(resp.output['embeddings'][0]['embedding'])
            return embedding
        else:
            raise Exception(f"GME API call failed: {resp.message}")

    def get_batch_embeddings(
        self, 
        texts: List[str] = None, 
        image_paths: List[str] = None,
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """Get batch multimodal embedding vectors
        
        Args:
            texts: List of texts
            image_paths: List of image paths
            batch_size: Batch size
            show_progress: Whether to show progress bar
            
        Returns:
            np.ndarray: Array of embedding vectors
        """
        if texts is None and image_paths is None:
            raise ValueError("texts and image_paths cannot be None at the same time")
            
        n = len(texts) if texts is not None else len(image_paths)
        embeddings = []
        
        iterator = range(0, n, batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc="Generating embedding vectors", unit="batch")
            
        for i in iterator:
            batch_texts = None if texts is None else texts[i:i+batch_size]
            batch_images = None if image_paths is None else image_paths[i:i+batch_size]
            
            batch_embeddings = []
            for j in range(min(batch_size, len(batch_texts or batch_images))):
                text = batch_texts[j] if batch_texts else None
                image = batch_images[j] if batch_images else None
                embedding = self.get_embedding(text, image)
                batch_embeddings.append(embedding)
                
            embeddings.extend(batch_embeddings)
            
        return np.array(embeddings)

    def get_text_embeddings(
        self, 
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """Get text embedding vectors
        
        Args:
            texts: List of texts
            batch_size: Batch size
            show_progress: Whether to show progress bar
            
        Returns:
            np.ndarray: Array of text embedding vectors
        """
        return self.get_batch_embeddings(
            texts=texts,
            image_paths=None,
            batch_size=batch_size,
            show_progress=show_progress
        )

    def get_image_embeddings(
        self,
        image_paths: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """Get image embedding vectors
        
        Args:
            image_paths: List of image paths
            batch_size: Batch size
            show_progress: Whether to show progress bar
            
        Returns:
            np.ndarray: Array of image embedding vectors
        """
        return self.get_batch_embeddings(
            texts=None,
            image_paths=image_paths,
            batch_size=batch_size,
            show_progress=show_progress
        )


class GmeQwen2VL:
    """GME Model Wrapper Class"""
    def __init__(
        self,
        model_name: str = "Alibaba-NLP/gme-Qwen2-VL-2B-Instruct",
        model_path: Optional[str] = None,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        min_image_tokens=256,
        max_image_tokens=1280,
        max_length=1800,
        **kwargs,
    ) -> None:
        model_name = model_path or model_name
        self.base = AutoModelForVision2Seq.from_pretrained(
            model_name, torch_dtype=torch.float16, **kwargs
        )
        self.base.eval()
        self.normalize = True
        self.device = device
        min_pixels = min_image_tokens * 28 * 28
        max_pixels = max_image_tokens * 28 * 28
        self.max_length = max_length
        self.processor = AutoProcessor.from_pretrained(
            model_name, min_pixels=min_pixels, max_pixels=max_pixels, **kwargs
        )
        self.processor.tokenizer.padding_side = 'right'
        self.default_instruction = 'You are a helpful assistant.'
        self.sep = ' '
        logger.info("Successfully initialized GME model")

    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[List[torch.FloatTensor]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        pixel_values: Optional[torch.Tensor] = None,
        image_grid_thw: Optional[torch.LongTensor] = None,
        pooling_mask: Optional[torch.LongTensor] = None,
        **kwargs
    ) -> torch.Tensor:
        if inputs_embeds is None:
            # Use the model's get_input_embeddings method
            inputs_embeds = self.base.get_input_embeddings()(input_ids)
            if pixel_values is not None:
                pixel_values = pixel_values.type(self.base.visual.get_dtype())
                image_embeds = self.base.visual(pixel_values, grid_thw=image_grid_thw).to(inputs_embeds.device)
                image_mask = input_ids == self.base.config.image_token_id
                inputs_embeds[image_mask] = image_embeds
            if attention_mask is not None:
                attention_mask = attention_mask.to(inputs_embeds.device)

        outputs = self.base.model(
            input_ids=None,
            position_ids=position_ids,
            attention_mask=attention_mask,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
        )

        pooling_mask = attention_mask if pooling_mask is None else pooling_mask
        left_padding = (pooling_mask[:, -1].sum() == pooling_mask.shape[0])
        if left_padding:
            embeddings = outputs.last_hidden_state[:, -1]
        else:
            sequence_lengths = pooling_mask.sum(dim=1) - 1
            batch_size = outputs.last_hidden_state.shape[0]
            embeddings = outputs.last_hidden_state[torch.arange(
                batch_size, device=outputs.last_hidden_state.device
            ), sequence_lengths]
        if self.normalize:
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings.contiguous()

    def embed(self, texts: list[str], images: list[Image.Image], is_query=True, instruction=None, **kwargs):
        self.base.to(self.device)
        input_texts, input_images = list(), list()
        for t, i in zip(texts, images):
            if not is_query or instruction is None:
                instruction = self.default_instruction
            input_str = ''
            if i is None:
                input_images = None
            else:
                input_str += '<|vision_start|><|image_pad|><|vision_end|>'
                i = self._fetch_image(i)
                input_images.append(i)
            if t is not None:
                input_str += t
            msg = f'<|im_start|>system\n{instruction}<|im_end|>\n<|im_start|>user\n{input_str}<|im_end|>\n<|im_start|>assistant\n<|endoftext|>'
            input_texts.append(msg)

        inputs = self.processor(
            text=input_texts,
            images=input_images,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            embeddings = self.forward(**inputs)
        return embeddings

    def _fetch_image(self, image: Union[str, Image.Image]) -> Image.Image:
        """Load image, supports local path, URL and PIL.Image object"""
        try:
            if isinstance(image, Image.Image):
                image_obj = image
            elif image.startswith(('http://', 'https://')):
                image_obj = Image.open(requests.get(image, stream=True).raw)
            elif image.startswith('file://'):
                image_obj = Image.open(image[7:])
            elif image.startswith('data:image'):
                if 'base64,' in image:
                    _, base64_data = image.split('base64,', 1)
                    data = base64.b64decode(base64_data)
                    image_obj = Image.open(BytesIO(data))
            else:
                image_obj = Image.open(image)

            if image_obj is None:
                raise ValueError(f"Unrecognized image input, support local path, http url, base64 and PIL.Image, got {image}")

            image = image_obj.convert('RGB')
            width, height = image.size
            resized_height, resized_width = self._smart_resize(height, width)
            image = image.resize((resized_width, resized_height))
            return image
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise

    def _smart_resize(
        self,
        height: int,
        width: int,
        factor: int = 28,
        min_pixels: int = 4 * 28 * 28,
        max_pixels: int = 16384 * 28 * 28,
        max_ratio: int = 200
    ) -> tuple[int, int]:
        """Smart resize image"""
        def round_by_factor(number: int, factor: int) -> int:
            return round(number / factor) * factor

        def ceil_by_factor(number: int, factor: int) -> int:
            return math.ceil(number / factor) * factor

        def floor_by_factor(number: int, factor: int) -> int:
            return math.floor(number / factor) * factor

        h_bar = max(factor, round_by_factor(height, factor))
        w_bar = max(factor, round_by_factor(width, factor))
        
        if h_bar * w_bar > max_pixels:
            beta = math.sqrt((height * width) / max_pixels)
            h_bar = floor_by_factor(height / beta, factor)
            w_bar = floor_by_factor(width / beta, factor)
        elif h_bar * w_bar < min_pixels:
            beta = math.sqrt(min_pixels / (height * width))
            h_bar = ceil_by_factor(height * beta, factor)
            w_bar = ceil_by_factor(width * beta, factor)

        if max(h_bar, w_bar) / min(h_bar, w_bar) > max_ratio:
            logger.warning(f"Absolute aspect ratio must be smaller than {max_ratio}, got {max(h_bar, w_bar) / min(h_bar, w_bar)}")
            if h_bar > w_bar:
                h_bar = w_bar * max_ratio
            else:
                w_bar = h_bar * max_ratio
        return h_bar, w_bar

    def get_text_embeddings(self, texts: List[str], instruction: Optional[str] = None, **kwargs) -> torch.Tensor:
        """Get text embeddings"""
        return self.get_fused_embeddings(texts=texts, instruction=instruction, **kwargs)

    def get_image_embeddings(self, images: List[Union[str, Image.Image]], is_query: bool = True, **kwargs) -> torch.Tensor:
        """Get image embeddings"""
        return self.get_fused_embeddings(images=images, is_query=is_query, **kwargs)

    def get_fused_embeddings(
        self,
        texts: Optional[List[str]] = None,
        images: Optional[List[Union[str, Image.Image]]] = None,
        batch_size: int = 32,
        show_progress_bar: bool = True,
        **kwargs
    ) -> torch.Tensor:
        """Get fused modal embeddings"""
        if isinstance(images, DataLoader):
            image_loader = images
            batch_size = image_loader.batch_size
            image_loader.dataset.transform = None
        else:
            if images is None:
                image_loader = None
            else:
                image_loader = DataLoader(
                    images,
                    batch_size=batch_size,
                    shuffle=False,
                    collate_fn=custom_collate_fn,
                    num_workers=0,  # Disable multi-process on Windows
                )

        if texts is None:
            assert image_loader is not None
            n_batch = len(image_loader)
        else:
            n_batch = len(texts) // batch_size + int(len(texts) % batch_size > 0)
            image_loader = image_loader or [None] * n_batch

        all_embeddings = list()
        none_batch = [None] * batch_size
        pbar = tqdm(total=n_batch, disable=not show_progress_bar, mininterval=1, miniters=10, desc='encode')
        
        for n, img_batch in zip(range(0, n_batch * batch_size, batch_size), image_loader):
            text_batch = none_batch if texts is None else texts[n: n+batch_size]
            img_batch = none_batch if img_batch is None else img_batch
            embeddings = self.embed(texts=text_batch, images=img_batch, **kwargs)
            pbar.update(1)
            all_embeddings.append(embeddings.cpu())
            
        pbar.close()
        all_embeddings = torch.cat(all_embeddings, dim=0)
        return all_embeddings 