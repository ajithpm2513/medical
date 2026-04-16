from pydantic import BaseModel
from typing import Optional, Dict


class MRIAnalysisResponse(BaseModel):
    label: str
    confidence: float
    report: str
    class_probabilities: Optional[Dict[str, float]] = None
    metadata: Optional[dict] = None
    heatmap_url: Optional[str] = None
    trust_score: Optional[float] = None
    consistency_check: Optional[str] = None
    auditor_notes: Optional[str] = None


class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    version: str
