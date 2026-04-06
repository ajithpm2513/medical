import os
import glob
import importlib.util
import torch
from ..core.config import get_settings


class ModelManager:
    """The Bridge: Reaches up into /models and /research folders."""

    def __init__(self):
        self.settings = get_settings()
        self.models_dir = self.settings.MODEL_PATH
        self.research_dir = self.settings.RESEARCH_PATH

    # ------------------------------------------------------------------ #
    #  Internal: resolve the _arch.py path for a given weight filename    #
    # ------------------------------------------------------------------ #
    def _resolve_arch_path(self, base: str) -> str | None:
        """Return the absolute path to the architecture script for `base`,
        trying an exact match first then falling back to the prefix token."""
        exact = os.path.join(self.research_dir, f"{base.lower()}_arch.py")
        fallback = os.path.join(self.research_dir, f"{base.split('_')[0].lower()}_arch.py")
        if os.path.exists(exact):
            return exact
        if os.path.exists(fallback):
            return fallback
        return None

    # Keyword → human-readable architecture label map (checked in order)
    _ARCH_LABELS = [
        ("triplefusion",  "Triple Fusion"),
        ("densenet121",   "DenseNet-121"),
        ("densenet",      "DenseNet"),
        ("mobilenet_v2",  "MobileNet-V2"),
        ("mobilenet",     "MobileNet"),
        ("resnet50",      "ResNet-50"),
        ("resnet",        "ResNet"),
        ("vit",           "Vision Transformer"),
        ("swin",          "Swin Transformer"),
        ("efficientnet",  "EfficientNet"),
    ]

    @classmethod
    def _arch_label(cls, base: str) -> str:
        """Return a human-friendly architecture name derived from the base filename."""
        lower = base.lower()
        for keyword, label in cls._ARCH_LABELS:
            if keyword in lower:
                return label
        return "Generic CNN"

    @staticmethod
    def _display_name(base: str) -> str:
        """Return a cleaned-up display name (title-cased, underscores removed)."""
        tokens = base.split('_')
        # Only strip the most generic prefix labels, keep version tokens like 'v2'
        cleaned = [t for t in tokens if t not in ('best', 'final')]
        return ' '.join(t.capitalize() for t in cleaned)


    # ------------------------------------------------------------------ #
    #  Discovery                                                           #
    # ------------------------------------------------------------------ #
    def get_local_models(self):
        """Scans /models for binary weights and returns frontend-ready objects."""
        extensions = {'.pth', '.h5', '.onnx', '.tflite'}
        model_list = []

        if not os.path.exists(self.models_dir):
            return []

        for filename in sorted(os.listdir(self.models_dir)):
            base, ext = os.path.splitext(filename)
            if ext not in extensions:
                continue

            model_list.append({
                "id":           filename,
                "name":         self._display_name(base),
                "architecture": self._arch_label(base),
                "extension":    ext.lstrip('.').upper(),   # "PTH", "ONNX" etc.
            })

        return model_list

    def list_available_architectures(self):
        return self.get_local_models()

    # ------------------------------------------------------------------ #
    #  Real model loading                                                  #
    # ------------------------------------------------------------------ #
    def load_weights(self, model_filename: str) -> torch.nn.Module:
        """Dynamically instantiate the architecture and load .pth weights.

        Steps
        -----
        1. Validate the weight file exists.
        2. Resolve the matching *_arch.py file via _resolve_arch_path().
        3. Import `get_model(num_classes=4)` from that file via importlib.
        4. Instantiate the model, load state_dict (CPU-mapped for portability).
        5. Set eval mode and return the live PyTorch Module.
        """
        model_path = os.path.join(self.models_dir, model_filename)
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Selected weights '{model_filename}' not found in /models."
            )

        base, _ = os.path.splitext(model_filename)
        arch_path = self._resolve_arch_path(base)

        if arch_path is None:
            raise ValueError(
                f"No architecture script found for '{model_filename}'. "
                "Please add a matching *_arch.py in /research."
            )

        # --- Dynamic import of the architecture module ---
        spec = importlib.util.spec_from_file_location("_dyn_arch", arch_path)
        arch_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(arch_module)

        # Every arch script must expose get_model(num_classes)
        if not hasattr(arch_module, "get_model"):
            raise AttributeError(
                f"Architecture script '{arch_path}' must define a "
                "`get_model(num_classes: int)` function."
            )

        model: torch.nn.Module = arch_module.get_model(num_classes=4)

        # --- Load weights (map to CPU for portability on grading machines) ---
        checkpoint = torch.load(model_path, map_location="cpu")

        # Support both raw state_dict and checkpoint dicts saved with metadata
        if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
            state_dict = checkpoint["model_state_dict"]
        else:
            state_dict = checkpoint

        model.load_state_dict(state_dict, strict=False)
        model.eval()
        return model
