import json
from typing import List, Optional
from pathlib import Path
import logging
from openai import OpenAI
import os
import base64
from PIL import Image, ImageDraw, ImageFont

from src.config.config import ProcessorConfig
from src.models.models import FunctionSegment, RAGResult
from src.models.gme_model import GmeQwen2VL, GmeAPI
from src.processors.rag_processor import RAGProcessor
from src.utils.logger import setup_logger

class ActionHistoryProcessor:
    """Action History Processor Class"""
    def __init__(self, config: ProcessorConfig):
        self.config = config
        self.logger = setup_logger(__name__, config.log_file, config.output_dir)
        
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout
        )
        
        try:
            # self.gme_model = GmeQwen2VL(config.model_name)
            self.gme_model = GmeAPI(config.gme_api_key)
            self.rag_processor = RAGProcessor(self.gme_model)
            self.logger.info("Successfully initialized processors")
        except Exception as e:
            self.logger.error(f"Failed to initialize processors: {str(e)}")
            raise
            
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 string"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _call_gpt4o(self, prompt: str, images: Optional[List[str]] = None) -> str:
        """Call GPT-4o model with multimodal input support"""
        messages = []
        
        # If there are image inputs, add image messages first
        if images:
            for image_path in images:
                base64_image = self._encode_image(image_path)
                messages.append({
                    "role": "user", 
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                })
        
        messages.append({
            "role": "user",
            "content": prompt
        })

        # print(messages)
        # print(prompt)
        
        for attempt in range(self.config.max_retries):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model="gpt-4o",
                )
                # print(chat_completion)
                return chat_completion.choices[0].message.content
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    self.logger.error(f"Error calling GPT-4o after {self.config.max_retries} attempts: {str(e)}")
                    raise
                self.logger.warning(f"Attempt {attempt + 1} failed, retrying...")

    def _extract_json_from_response(self, response: str) -> dict:
        """Extract JSON from response"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            json_str = response[start:end]
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Failed to parse JSON from response: {str(e)}")
            raise

    def _compress_image(self, image: Image.Image, quality: int = 60, max_size: tuple = (800, 800)) -> Image.Image:
        """Compress image quality and size
        
        Args:
            image: Original image
            quality: JPEG compression quality (1-100)
            max_size: Maximum size (width, height)
        """
        # Resize image
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Create new RGB image (remove alpha channel)
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        
        return image

    def segment_by_function(self, actions: List[str], screenshots: List[str]) -> List[FunctionSegment]:
        """Segment history by function"""
        if len(screenshots) != len(actions) + 1:
            raise ValueError(f"Invalid input: screenshots length ({len(screenshots)}) should be actions length ({len(actions)}) + 1")
            
        segments = []
        current_index = 0
        
        while current_index < len(actions):
            try:
                end_index = min(current_index + self.config.window_size, len(actions))
                window_actions = actions[current_index:end_index]
                window_screenshots = screenshots[current_index:end_index + 1]

                prompt = self._build_segmentation_prompt(window_actions, current_index, end_index)
                
                # Process images and save to temporary files
                temp_image_paths = []
                for i, screenshot in enumerate(window_screenshots):
                    # Open original image
                    image = Image.open(screenshot)
                    # Compress image
                    compressed_image = self._compress_image(image)
                    # Create a new image copy
                    marked_image = compressed_image.copy()
                    draw = ImageDraw.Draw(marked_image)
                    
                    # Use larger font and more prominent color
                    font = ImageFont.truetype("arial.ttf", 48)  # Increase font size
                    # Add white background box
                    text_bbox = draw.textbbox((20, 20), str(i), font=font)
                    draw.rectangle([text_bbox[0]-20, text_bbox[1]-20, text_bbox[2]+20, text_bbox[3]+20],  # Increase background box margin
                                 fill='white')
                    # Draw large text in red
                    draw.text((20, 20), str(i), font=font, fill='red')
                    
                    # Save marked image to temporary file
                    os.makedirs("tmp/", exist_ok=True)
                    temp_path = f"tmp/temp_screenshot_{i}.png"
                    marked_image.save(temp_path, 'JPEG', quality=60, optimize=True)
                    temp_image_paths.append(temp_path)
                    
                    # Verify if image was saved correctly
                    saved_image = Image.open(temp_path)
                    if saved_image.getbbox() != marked_image.getbbox():
                        self.logger.warning(f"Image {i} may not have been saved correctly")

                response = self._call_gpt4o(prompt, temp_image_paths)
                result = self._extract_json_from_response(response)
                segment = FunctionSegment(
                    actions=window_actions[:result['end_index']],
                    screenshots=window_screenshots[:result['end_index'] + 1],
                    func_desc=result['func_desc'],
                    action_detail=result['action_detail'],
                    reasoning=result['reasoning']
                )
                segments.append(segment)
                
                current_index += result['end_index']
                self.logger.info(f"Successfully processed segment {len(segments)}")
                
                # Clean up temporary files
                for temp_path in temp_image_paths:
                    try:
                        os.remove(temp_path)
                    except Exception as e:
                        self.logger.warning(f"Failed to remove temporary file {temp_path}: {str(e)}")
                
            except Exception as e:
                self.logger.error(f"Error processing segment at index {current_index}: {str(e)}")
                raise
                
        return segments

    def summarize_functions(self, segments: List[FunctionSegment]) -> str:
        """Summarize all functions"""
        # print("summarize all functions")
        prompt = self._build_summary_prompt(segments)
        # print("prompt:")
        # print(prompt)
        response = self._call_gpt4o(prompt)
        # print("response:")
        # print(response)
        return response

    def _build_segmentation_prompt(self, actions: List[str], current_index: int, end_index: int) -> str:
        """Build function segmentation prompt"""
        # enumerate from current_index to end_index
        actions_str = ""
        for i in range(end_index - current_index):
            actions_str += f"{i + current_index}: {actions[i]}\n"
        return f"""Please analyze the following sequence of actions and screenshots from an Android app.
Actions: 
{actions_str}

The screenshot index is displayed in the upper left corner of the screenshot.

Please identify where a logical function or small task ends in this sequence.
Return your analysis in the following JSON format:
```json
{{
    "end_index": <index where the function ends>,
    "func_desc": "Detailed description of the identified function",
    "action_detail": "Detailed description of the action of this function",
    "reasoning": "Detailed reasoning for why this is a complete function"
}}
```

Consider:
1. UI state changes
2. Logical task completion
3. User intention
4. App flow
"""

    def _build_summary_prompt(self, segments: List[FunctionSegment]) -> str:
        """Build function summary prompt"""
        segments_info = []
        for segment in segments:
            segments_info.append({
                "func_desc": segment.func_desc,
                "action_detail": segment.action_detail
            })
            
        return f"""Please analyze the following function segments from an Android app and provide a comprehensive summary.
Function segments: {json.dumps(segments_info, ensure_ascii=False)}

Please provide a detailed summary including:
1. Overall app interface analysis
2. Main functionalities
3. Testing recommendations for:
   - Coverage testing
   - Bug detection
   - Edge cases
   - Critical paths

Format your response as a detailed text analysis.
"""

    def process_and_save(self, actions: List[str], screenshots: List[str], 
                        output_file: Optional[str] = None) -> None:
        """Process history and save results"""
        try:
            if output_file is None:
                output_file = Path(self.config.output_dir) / "app_analysis.txt"
            else:
                output_file = Path(output_file)
            
            segments = self.segment_by_function(actions, screenshots)
            
            summary = self.summarize_functions(segments)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(summary)
                
            segments_data = []
            for segment in segments:
                segments_data.append({
                    'actions': segment.actions,
                    'screenshots': segment.screenshots,
                    'func_desc': segment.func_desc,
                    'action_detail': segment.action_detail,
                    'reasoning': segment.reasoning
                })
                
            segments_file = output_file.parent / 'segments_data.json'
            with open(segments_file, 'w', encoding='utf-8') as f:
                json.dump(segments_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"Successfully saved results to {output_file} and {segments_file}")
            
        except Exception as e:
            self.logger.error(f"Error in process_and_save: {str(e)}")
            raise
            
    def search_rag(self, query_text: Optional[str] = None, 
                  query_image: Optional[str] = None, 
                  k: int = 3) -> List[RAGResult]:
        """Search RAG knowledge base"""
        return self.rag_processor.search(query_text, query_image, k) 