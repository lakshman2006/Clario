from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    topic: str

class RecommendationItem(BaseModel):
    title: str
    type: str
    url: str
    confidence: float

class RecommendationResponse(BaseModel):
    status: str
    message: str
    data: List[RecommendationItem]

class ErrorResponse(BaseModel):
    status: str
    message: str
    error_code: Optional[str] = None
