import os
import json
import re
import numpy as np
from PIL import Image

OUTPUT_IMAGE = "/root/anthropic_branded_artifact.png"
OUTPUT_META = "/root/design_parameters.json"

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

EXPECTED_HEX_VALUES = {
    "background_hex": "#faf9f5",
    "corporate_dark_hex": "#141413",
    "primary_accent_hex": "#d97757",
}

EXPECTED_HEADING_FONT_SUBSTRING = "Poppins"

REQUIRED_KEYS = {
    "background_hex",
    "corporate_dark_hex",
    "primary_accent_hex",
    "applied_heading_font",
}


def hex_to_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


def load_metadata():
    with open(OUTPUT_META, "r", encoding="utf-8") as f:
        return json.load(f)


def load_image_rgb():
    img = Image.open(OUTPUT_IMAGE).convert("RGB")
    arr = np.array(img)
    return img, arr, arr.reshape(-1, 3)


def load_image_hsv():
    img = Image.open(OUTPUT_IMAGE).convert("HSV")
    return np.array(img)


def color_presence_ratio(pixels: np.ndarray, hex_color: str, tolerance: float = 15.0) -> float:
    target = hex_to_rgb(hex_color)
    distances = np.linalg.norm(pixels.astype(np.float32) - target, axis=1)
    return float(np.mean(distances < tolerance))


def test_files_exist():
    assert os.path.exists(OUTPUT_IMAGE), f"Missing image file: {OUTPUT_IMAGE}"
    assert os.path.exists(OUTPUT_META), f"Missing metadata file: {OUTPUT_META}"


def test_design_parameters_exact_schema_and_values():
    data = load_metadata()

    assert set(data.keys()) == REQUIRED_KEYS, (
        f"design_parameters.json must contain exactly these keys: {sorted(REQUIRED_KEYS)}; "
        f"got: {sorted(data.keys())}"
    )

    for k in REQUIRED_KEYS - {"applied_heading_font"}:
        assert isinstance(data[k], str), f"{k} must be a string"
        assert HEX_RE.match(data[k]), f"{k} must be a valid #RRGGBB hex color, got: {data[k]}"
        assert data[k].lower() == EXPECTED_HEX_VALUES[k], (
            f"{k} should be {EXPECTED_HEX_VALUES[k]}, got: {data[k]}"
        )

    assert isinstance(data["applied_heading_font"], str) and data["applied_heading_font"].strip(), (
        "applied_heading_font must be a non-empty font name"
    )


def test_heading_font_matches_expected_corporate_font():
    data = load_metadata()
    font_name = data["applied_heading_font"]
    assert EXPECTED_HEADING_FONT_SUBSTRING.lower() in font_name.lower(), (
        f"Expected heading font to include '{EXPECTED_HEADING_FONT_SUBSTRING}', got: {font_name}"
    )


def test_declared_brand_hexes_actually_appear_in_image():
    """
    Prevent metadata-only hallucination: every declared brand HEX should have
    at least a small but real presence in the rendered poster.

    We keep this as an existence check rather than a strong area requirement,
    because some required brand colors may be used only for thin leader lines
    or compact connector details.
    """
    data = load_metadata()
    _, _, pixels = load_image_rgb()

    min_visible_ratio = 1e-5  # ~10 px per megapixel; enough to prove real usage without over-constraining layout

    for key in REQUIRED_KEYS - {"applied_heading_font"}:
        ratio = color_presence_ratio(pixels, data[key], tolerance=15)
        assert ratio > min_visible_ratio, (
            f"{key} is declared in JSON but does not appear meaningfully in the image "
            f"(ratio={ratio:.6f})"
        )


def test_background_color_detected_in_image():
    data = load_metadata()
    _, rgb_arr, pixels = load_image_rgb()
    bg_hex = data["background_hex"]

    global_bg_ratio = color_presence_ratio(pixels, bg_hex, tolerance=15)
    assert global_bg_ratio > 0.20, (
        f"Background color not sufficiently present in image (ratio={global_bg_ratio:.4f})"
    )

    h, w, _ = rgb_arr.shape
    patch = max(12, min(h, w) // 18)

    corners = {
        "top_left": rgb_arr[0:patch, 0:patch],
        "top_right": rgb_arr[0:patch, w - patch:w],
        "bottom_left": rgb_arr[h - patch:h, 0:patch],
        "bottom_right": rgb_arr[h - patch:h, w - patch:w],
    }

    for name, region in corners.items():
        ratio = color_presence_ratio(region.reshape(-1, 3), bg_hex, tolerance=15)
        assert ratio > 0.65, f"{name} corner is not dominated by background color (ratio={ratio:.4f})"


def test_minimalist_low_saturation_and_no_neon():
    hsv = load_image_hsv()
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    avg_saturation = float(np.mean(s))
    assert avg_saturation < 90, (
        f"Image is too saturated ({avg_saturation:.2f}), likely ignored minimalist constraint."
    )

    neon_like_ratio = float(np.mean((s > 180) & (v > 180)))
    assert neon_like_ratio < 0.01, (
        f"Too many high-saturation bright pixels ({neon_like_ratio:.4%}); image may contain neon/AI-gradient styling."
    )