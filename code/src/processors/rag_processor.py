import faiss
import numpy as np
from typing import List, Optional
import logging
from pathlib import Path

from src.models.models import FunctionSegment, RAGResult
from src.models.gme_model import GmeQwen2VL, GmeAPI

logger = logging.getLogger(__name__)

class RAGProcessor:
    """RAG Processor Class"""
    def __init__(self, gme_model: GmeAPI):
        self.gme_model = gme_model
        self.text_index = None
        self.image_index = None
        self.segments = []
        
    def build_index(self, segments: List[FunctionSegment]) -> None:
        """Build RAG index"""
        try:
            self.segments = segments
            
            # Prepare text data
            text_data = []
            for segment in segments:
                text_data.append(f"{segment.func_desc} {segment.reasoning}")
            
            # Prepare image data
            image_data = []
            for segment in segments:
                image_data.extend(segment.screenshots)
            
            # Verify image files exist
            for image_path in image_data:
                if not Path(image_path).exists():
                    raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Generate text embeddings
            text_embeddings = self.gme_model.get_text_embeddings(
                texts=text_data,
            )
            
            # Generate image embeddings
            image_embeddings = self.gme_model.get_image_embeddings(
                image_paths=image_data,
            )
            
            # Create FAISS indices
            dimension = text_embeddings.shape[1]
            self.text_index = faiss.IndexFlatL2(dimension)
            self.image_index = faiss.IndexFlatL2(dimension)
            
            # Add embeddings to indices
            self.text_index.add(text_embeddings)
            self.image_index.add(image_embeddings)
            
            logger.info(f"Successfully built RAG index with {len(segments)} segments")
            
        except Exception as e:
            logger.error(f"Error building RAG index: {str(e)}")
            raise
            
    def search(self, query_text: Optional[str] = None, 
              query_image: Optional[str] = None, 
              k: int = 3) -> List[RAGResult]:
        """Search RAG knowledge base"""
        if query_text is None and query_image is None:
            raise ValueError("Either query_text or query_image must be provided")
            
        results = []
        
        # Text search
        if query_text:
            query_text_embedding = self.gme_model.get_text_embeddings(
                texts=[query_text]
            )
            D_text, I_text = self.text_index.search(query_text_embedding, k)
            
            for i, (distance, idx) in enumerate(zip(D_text[0], I_text[0])):
                results.append(RAGResult(
                    segment=self.segments[idx],
                    similarity_score=float(1 / (1 + distance)),
                    match_type='text'
                ))
        
        # Image search
        if query_image:
            query_image_embedding = self.gme_model.get_image_embeddings(
                images=[query_image],
                is_query=True
            )
            D_image, I_image = self.image_index.search(query_image_embedding, k)
            
            for i, (distance, idx) in enumerate(zip(D_image[0], I_image[0])):
                # Find corresponding segment
                segment_idx = idx // len(self.segments[0].screenshots)
                results.append(RAGResult(
                    segment=self.segments[segment_idx],
                    similarity_score=float(1 / (1 + distance)),
                    match_type='image'
                ))
        
        # Merge and sort results
        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:k] 