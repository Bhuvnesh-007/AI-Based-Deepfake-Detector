import os
import torch
import torch.nn as nn
import timm
from torchvision import transforms
from PIL import Image

# ---------------------------------------------------------------
# CONFIG — Adjust these to match how you trained your model
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

    model = timm.create_model(VIT_MODEL_NAME, pretrained=False, num_classes=NUM_CLASSES)
    return model


def _strip_state_dict_prefix(state_dict, reference_model):
    """
    Some training scripts save the checkpoint from a wrapper object instead
    of the bare timm model directly, e.g.:

        class DeepfakeDetector(nn.Module):
            def __init__(self):
                self.backbone = timm.create_model(...)   # -> keys prefixed "backbone."

    or from nn.DataParallel / DistributedDataParallel, which prefixes every
    key with "module.". When that happens, load_state_dict(strict=True)
    fails with "Missing key(s)" for every single layer, because the plain
    architecture has keys like "patch_embed.proj.weight" but the checkpoint
    has "backbone.patch_embed.proj.weight" (or "module.patch_embed...").

    This detects that situation and strips the offending prefix so the keys
    line up again.
    """
    ref_keys = set(reference_model.state_dict().keys())
    ckpt_keys = list(state_dict.keys())

    # Already matching — nothing to do.
    if any(k in ref_keys for k in ckpt_keys):
        return state_dict

    # Try common wrapper prefixes, plus auto-detect any shared single prefix
    # (e.g. "backbone.", "vit.", "encoder.") by comparing the first segment
    # of the checkpoint keys against the reference keys.
    candidate_prefixes = ["module.", "model.", "backbone.", "vit.", "net."]

    # Auto-detect: if every checkpoint key shares the same first path
    # segment (e.g. "backbone.xxx"), and stripping it produces keys that
    # exist in the reference model, add it as a candidate.
    first_segments = {k.split(".", 1)[0] for k in ckpt_keys if "." in k}
    if len(first_segments) == 1:
        auto_prefix = f"{next(iter(first_segments))}."
        if auto_prefix not in candidate_prefixes:
            candidate_prefixes.append(auto_prefix)

    for prefix in candidate_prefixes:
        stripped = {
            (k[len(prefix):] if k.startswith(prefix) else k): v
            for k, v in state_dict.items()
        }
        if any(k in ref_keys for k in stripped.keys()):
            print(f"[model_utils] Detected checkpoint keys prefixed with "
                  f"'{prefix}' — stripping prefix before loading.")
            return stripped

    # No known prefix matched — return unchanged and let load_state_dict
    # raise its normal (now more informative) error.
    return state_dict


def load_model():

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

            # Fix up key names if the checkpoint was saved from a wrapped
            # module (module./backbone./model. prefix etc.) — this is the
            # cause of "Missing key(s) ... patch_embed.proj.weight" style
            # errors when the underlying weights are otherwise compatible.
            state_dict = _strip_state_dict_prefix(state_dict, model)

            try:
                missing, unexpected = model.load_state_dict(state_dict, strict=True)
            except RuntimeError as strict_err:
                # Give a much more actionable error than the raw torch
                # message: show what strict=False would report, so it's
                # clear whether this is a real architecture mismatch or
                # just leftover/renamed keys.
                loose_missing, loose_unexpected = model.load_state_dict(state_dict, strict=False)
                raise RuntimeError(
                    "State dict does not match model architecture.\n"
                    f"  Missing keys ({len(loose_missing)}): {loose_missing[:5]}"
                    f"{' ...' if len(loose_missing) > 5 else ''}\n"
                    f"  Unexpected keys ({len(loose_unexpected)}): {loose_unexpected[:5]}"
                    f"{' ...' if len(loose_unexpected) > 5 else ''}\n"
                    "If 'Unexpected keys' shows names like 'backbone.xxx' or "
                    "'module.xxx', the checkpoint was saved from a wrapped "
                    "model — update VIT_MODEL_NAME/build_model_architecture "
                    "or the prefix list in _strip_state_dict_prefix to match. "
                    "If keys look completely unrelated (e.g. conv/resnet-style "
                    "names), this checkpoint was not trained with "
                    "vit_base_patch16_224 and VIT_MODEL_NAME needs to change."
                ) from strict_err
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
