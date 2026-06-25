"""
model_utils.py
PyTorch model loading + inference for the Deepfake Detector.

Configured for: timm ViT-Base/16 (vit_base_patch16_224), num_classes=2,
weights saved as a state_dict. Confirmed via the actual checkpoint's
head.weight shape ([2, 768]) and class folders 'fake'/'real' sorted
alphabetically by ImageFolder -> index 0 = fake, index 1 = real.

============================================================
  WHERE TO PLUG IN YOUR TRAINED MODEL
============================================================
1. Drop your trained weights file into:  model/deepfake_model.pth
   (or change MODEL_PATH below to point wherever you keep it)

2. If your ViT variant, image size, or num_classes differs from the
   defaults below, update VIT_MODEL_NAME / IMAGE_SIZE / NUM_CLASSES.

3. Adjust `IMAGE_SIZE` and `transform` if your model was trained with
   different input size / normalization stats than the ImageNet
   defaults used here.

4. Adjust `predict()` if your model's output isn't a single sigmoid
   logit for "fake probability" (e.g. if it's a 2-class softmax,
   see the commented alternative inside predict()).
============================================================
"""

import os
import torch
import torch.nn as nn
import timm
from torchvision import transforms
from PIL import Image

# ---------------------------------------------------------------
# CONFIG — adjust these to match how you trained your model
# ---------------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "deepfake_model.pth")
VIT_MODEL_NAME = "vit_base_patch16_224"  # timm model name for ViT-Base/16
NUM_CLASSES = 2  # confirmed from checkpoint error: head.weight shape is [2, 768] -> 2-class softmax [real, fake]
IMAGE_SIZE = 224  # standard for vit_base_patch16_224 — change only if you trained at a different resolution
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Standard ImageNet normalization — change if you trained with different stats
transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def build_model_architecture():
    """
    Builds the ViT-Base/16 architecture (timm) that matches your trained
    weights' state_dict structure (confirmed via key inspection:
    cls_token, pos_embed, patch_embed.*, blocks.0-11.*, norm.*, head.*).
    """
    model = timm.create_model(VIT_MODEL_NAME, pretrained=False, num_classes=NUM_CLASSES)
    return model


def load_model():
    """
    Loads the trained PyTorch model from MODEL_PATH.
    Returns (model, error_message) where:
      - model is None and error_message is None if no weights file exists yet
        (clean 'demo mode' before you've added weights)
      - model is None and error_message is a string if the file exists but
        failed to load (so the UI can show you the REAL error instead of
        silently falling back to demo mode)
      - model is the loaded nn.Module and error_message is None on success
    """
    if not os.path.exists(MODEL_PATH):
        return None, None

    try:
        checkpoint = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)

        # checkpoint is a raw state_dict (OrderedDict of tensors) — build the
        # architecture and load the weights into it.
        if isinstance(checkpoint, dict):
            # Some training scripts wrap the state_dict inside a larger
            # checkpoint dict, e.g. {"model_state_dict": ..., "epoch": ...}.
            # Handle both the raw state_dict case and that wrapped case.
            state_dict = checkpoint.get("state_dict") or checkpoint.get("model_state_dict") or checkpoint

            model = build_model_architecture()
            missing, unexpected = model.load_state_dict(state_dict, strict=True)
        else:
            # Full model object was saved directly.
            model = checkpoint

        model.to(DEVICE)
        model.eval()
        return model, None
    except Exception as e:
        error_message = f"{type(e).__name__}: {e}"
        print(f"[model_utils] Failed to load model: {error_message}")
        return None, error_message


def preprocess_image(pil_image: Image.Image) -> torch.Tensor:
    """Convert a PIL image into a normalized tensor batch of shape (1, 3, H, W)."""
    img = pil_image.convert("RGB")
    tensor = transform(img)
    return tensor.unsqueeze(0).to(DEVICE)


@torch.no_grad()
def predict(model, pil_image: Image.Image) -> dict:
    """
    Runs inference and returns a result dict:
        {
            "label": "FAKE" or "REAL",
            "confidence": float 0-100,
            "raw_score": float 0-1   (probability the image is AI-generated/fake)
        }

    If model is None (no weights uploaded yet), returns a clearly-flagged
    demo placeholder so the UI still works end-to-end.
    """
    if model is None:
        # ---- Demo mode placeholder (no real model loaded) ----
        import random
        raw_score = random.uniform(0.55, 0.95)
        label = "FAKE" if raw_score >= 0.5 else "REAL"
        confidence = raw_score * 100 if label == "FAKE" else (1 - raw_score) * 100
        return {"label": label, "confidence": round(confidence, 1), "raw_score": raw_score, "demo": True}

    input_tensor = preprocess_image(pil_image)
    output = model(input_tensor)  # shape: [1, 2] for ViT-Base with num_classes=2

    # Confirmed class mapping from ImageFolder alphabetical sort of
    # 'fake'/'real' folder names: index 0 = fake, index 1 = real.
    probs = torch.softmax(output, dim=1)[0]
    fake_prob = probs[0].item()
    raw_score = fake_prob  # "raw_score" = probability the image is fake

    label = "FAKE" if raw_score >= 0.5 else "REAL"
    confidence = raw_score * 100 if label == "FAKE" else (1 - raw_score) * 100

    return {"label": label, "confidence": round(confidence, 1), "raw_score": raw_score, "demo": False}
