from pydantic import BaseModel
from typing import Optional, List

class MRIAnalysisResponse(BaseModel):
    label: str
    confidence: float
    report: str
    metadata: Optional[dict] = None

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    version: str
