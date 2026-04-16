import time
import asyncio
import torch
import torch.nn.functional as F
import numpy as np
import cv2

from fastapi import APIRouter, UploadFile, File, HTTPException

from ..schemas.mri_schema import MRIAnalysisResponse
from ..services.preprocessor import MRIPreprocessor
from ..services.model_loader import ModelManager
from ..core.config import get_settings
from ..services.reporter import MedicalReporter, ReportAuditor

settings = get_settings()
reporter = MedicalReporter()
auditor = ReportAuditor()
router = APIRouter(prefix="/classify", tags=["Laboratory Analysis"])


@router.post("/", response_model=MRIAnalysisResponse)
async def classify_mri_scan(
    file: UploadFile = File(...),
    model_id: str = "best_resnet50.pth",
):
    """Real PyTorch inference endpoint for MRI classification."""

    # ── 1. Load model (validates file exists + returns live nn.Module) ──
    manager = ModelManager()
    try:
        t_load_start = time.time()
        model = manager.load_weights(model_id)
        load_ms = int((time.time() - t_load_start) * 1000)
    except (FileNotFoundError, ValueError, AttributeError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model loading error: {str(e)}")

    # ── 2. Decode uploaded image ─────────────────────────────────────────
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise HTTPException(status_code=400, detail="Corrupted or unreadable MRI image.")

    # ── 3. Preprocess → (1, 3, 224, 224) normalised tensor ───────────────
    try:
        tensor = MRIPreprocessor.prepare_tensor(image_bgr)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Preprocessing failed: {str(e)}")

    # ── 4. Real inference ─────────────────────────────────────────────────
    t_infer_start = time.time()
    with torch.no_grad():
        logits = model(tensor)          # shape: (1, num_classes)
    infer_ms = int((time.time() - t_infer_start) * 1000)

    probs = F.softmax(logits, dim=1)[0]      # shape: (num_classes,)
    predicted_idx = int(torch.argmax(probs).item())
    confidence = float(probs[predicted_idx].item())

    label = settings.CLASS_MAPPING.get(predicted_idx, "Unknown Pathology")

    # Build per-class probability dict for the response
    class_probabilities = {
        settings.CLASS_MAPPING[i]: round(float(probs[i].item()), 4)
        for i in range(len(probs))
    }

    # ── 5. Grad-CAM++ (only for the TripleFusion model) ──────────────────
    heatmap_url = None
    _TRIPLE_FUSION_ID = "Final_TripleFusion_99Acc.pth"

    if model_id == _TRIPLE_FUSION_ID:
        try:
            heatmap_url = ModelManager.generate_gradcam(
                model=model,
                input_tensor=tensor,
                original_image_bgr=image_bgr,
                predicted_class_idx=predicted_idx,
            )
            # Append cache-buster so browser always fetches the latest heatmap
            heatmap_url = f"{heatmap_url}?t={int(time.time())}"
        except Exception as e:
            # Non-fatal: log but don't block the classification result
            import traceback
            traceback.print_exc()
            heatmap_url = None

    # ── 6. Generate Llama-3 clinical report ───────────────────────────────
    clinical_report = reporter.generate_medical_report(label, confidence)

    # ── 7. Hallucination Detection — async audit ─────────────────────────
    try:
        audit = await asyncio.to_thread(
            auditor.audit_report, label, clinical_report
        )
    except Exception:
        audit = {
            "trust_score": None,
            "consistency_check": None,
            "auditor_notes": "Audit unavailable.",
        }

    return MRIAnalysisResponse(
        label=f"{label} Detected",
        confidence=round(confidence, 4),
        report=clinical_report,
        class_probabilities=class_probabilities,
        heatmap_url=heatmap_url,
        trust_score=audit.get("trust_score"),
        consistency_check=audit.get("consistency_check"),
        auditor_notes=audit.get("auditor_notes"),
        metadata={
            "model_id": model_id,
            "predicted_class_idx": predicted_idx,
            "load_ms": load_ms,
            "inference_ms": infer_ms,
            "engine": "PyTorch (CPU)",
        },
    )


@router.get("/models")
async def list_models():
    """Returns dynamic list of discovered weight files from /models."""
    manager = ModelManager()
    return manager.list_available_architectures()
