from fastapi import APIRouter
from ..services.reporter import MedicalReporter
from ..schemas.mri_schema import MRIAnalysisResponse

router = APIRouter(prefix="/reporter", tags=["LLM Services"])
reporter_service = MedicalReporter()

@router.get("/generate")
async def generate_demo_report(label: str, confidence: float):
    """Standalone endpoint for high-precision clinical report generation."""
    return {"report": reporter_service.generate_medical_report(label, confidence)}
