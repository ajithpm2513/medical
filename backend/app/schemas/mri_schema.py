from pydantic import BaseModel
from typing import Optional, Dict


class MRIAnalysisResponse(BaseModel):
    label: str
    confidence: float
    report: str
    class_probabilities: Optional[Dict[str, float]] = None
    metadata: Optional[dict] = None


class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    version: str
