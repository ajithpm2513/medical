import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api import classify, reporter
from .core.config import get_settings

# Theoretical imports for Phase 2
# from .api import auth

settings = get_settings()

# Resolve the backend root directory (…/backend/)
_BACKEND_ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Professional MRI Diagnostic Terminal for Clinical Image Classification."
)

# Enable CORS for React Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup: ensure heatmap output directory exists ──────────────────
@app.on_event("startup")
async def create_heatmap_directory():
    heatmap_dir = _BACKEND_ROOT / "static" / "heatmaps"
    heatmap_dir.mkdir(parents=True, exist_ok=True)

# ── Serve static files (heatmaps, etc.) ──────────────────────────────
static_dir = _BACKEND_ROOT / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include API Routers
app.include_router(classify.router)
app.include_router(reporter.router)

@app.get("/health", tags=["Diagnostic Dashboard"])
async def health_check():
    """System health and diagnostic status."""
    return {
        "status": "Healthy",
        "system": settings.APP_NAME,
        "database": "Operational",
        "classification_engine": "Loaded",
        "LLM_module": "Ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
