import os
import glob
from ..core.config import get_settings

class ModelManager:
    """The Bridge: Reaches up into /models and /research folders."""
    
    def __init__(self):
        self.settings = get_settings()
        self.models_dir = self.settings.MODEL_PATH
        self.research_dir = self.settings.RESEARCH_PATH

    def get_local_models(self):
        """Scans the /models directory for binary weights with common ML extensions."""
        extensions = {'.pth', '.h5', '.onnx', '.tflite'}
        model_list = []
        
        # Physical scan of the directory
        if not os.path.exists(self.models_dir):
            return []

        for filename in os.listdir(self.models_dir):
            base, ext = os.path.splitext(filename)
            if ext in extensions:
                # Part A: Architecture Mapping (Bridge to /research)
                # Logic: Look for {base.lower()}_arch.py first, then fallback to {base.split('_')[0].lower()}_arch.py
                exact_arch_path = os.path.join(self.research_dir, f"{base.lower()}_arch.py")
                fallback_arch_path = os.path.join(self.research_dir, f"{base.split('_')[0].lower()}_arch.py")
                
                if os.path.exists(exact_arch_path):
                    arch_path = exact_arch_path
                    has_architecture = True
                else:
                    arch_path = fallback_arch_path
                    has_architecture = os.path.exists(fallback_arch_path)
                
                model_list.append({
                    "id": filename,
                    "name": base.replace('_', ' ').title(),
                    "architecture": os.path.basename(arch_path) if has_architecture else "Generic (ViT)",
                    "extension": ext,
                    "path": os.path.join(self.models_dir, filename)
                })
        
        return model_list

    def list_available_architectures(self):
        """Discovers architectures in the /models directory for the UI."""
        return self.get_local_models()

    def load_weights(self, model_filename: str):
        """Loads physical weights from /models/{filename}."""
        model_path = os.path.join(self.models_dir, model_filename)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Selected weights '{model_filename}' not discovered in /models database.")
        
        # Bridge logic: In Phase 2, this will instantiate the class from /research
        return {"filename": model_filename, "status": "Ready for Physiological Inference"}
