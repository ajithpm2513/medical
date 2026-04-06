import cv2
import numpy as np
import torch

# ImageNet normalization constants (standard for DenseNet, ResNet, MobileNet backbones)
_IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
_IMAGENET_STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)


class MRIPreprocessor:
    """Medical-grade MRI pre-processing pipeline.

    Pipeline:
        Raw BGR image from OpenCV
        → Ensure 3-channel RGB
        → Resize to 224×224
        → 0-1 min-max scaling
        → ImageNet mean/std normalisation
        → PyTorch Tensor (1, 3, 224, 224)
    """

    @staticmethod
    def normalize_dicom(pixel_array: np.ndarray) -> np.ndarray:
        """Standardize intensities to [0, 1]."""
        min_val = np.min(pixel_array)
        max_val = np.max(pixel_array)
        if max_val - min_val == 0:
            return np.zeros_like(pixel_array, dtype=np.float32)
        return ((pixel_array - min_val) / (max_val - min_val)).astype(np.float32)

    @staticmethod
    def resize_for_vision_transformer(
        image: np.ndarray, target_size=(224, 224)
    ) -> np.ndarray:
        """Resize to the standard transformer / CNN input size."""
        return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def prepare_tensor(image_bgr: np.ndarray) -> torch.Tensor:
        """Full clinical preprocessing pipeline → PyTorch Tensor (1, 3, 224, 224).

        Args:
            image_bgr: Raw OpenCV image in BGR format.
        Returns:
            Normalised float32 tensor ready for model inference.
        """
        # Step 1 – Convert grayscale MRIs to 3-channel RGB
        if len(image_bgr.shape) == 2:
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # Step 2 – Resize to 224×224
        image_rgb = cv2.resize(image_rgb, (224, 224), interpolation=cv2.INTER_LINEAR)

        # Step 3 – 0-1 min-max scaling
        image_f = image_rgb.astype(np.float32) / 255.0

        # Step 4 – ImageNet mean/std normalisation (channel-wise)
        image_f = (image_f - _IMAGENET_MEAN) / _IMAGENET_STD

        # Step 5 – HWC → CHW, add batch dimension → (1, 3, 224, 224)
        tensor = torch.from_numpy(image_f.transpose(2, 0, 1)).unsqueeze(0)
        return tensor  # dtype: float32
