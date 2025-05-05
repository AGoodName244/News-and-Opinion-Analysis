from pydantic import BaseModel
from typing import List

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    sentiment: str
    keywords: List[str]
    summary: str