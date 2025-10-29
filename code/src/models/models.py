from dataclasses import dataclass
from typing import List

@dataclass
class FunctionSegment:
    """Function segment data class"""
    actions: List[str]
    screenshots: List[str]
    func_desc: str
    action_detail: str
    reasoning: str

@dataclass
class RAGResult:
    """RAG search result data class"""
    segment: FunctionSegment
    similarity_score: float
    match_type: str  # 'text', 'image', or 'both' 