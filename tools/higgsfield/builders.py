"""Per-model param builders for ``higgsfield_generate``.

Each builder mirrors ``generation/<model>.go:run<Model>FromInput`` in the Go
``higgsfieldcli``. Inputs and defaults match so existing JSON payloads work
unchanged.

Layout: helpers → dimension tables → per-model enum tables → builder
functions (grouped by family) → ``BUILDERS`` dispatch table.

The dispatch table maps the JSON ``model`` discriminator to
``(api_model_name, builder_fn)``. ``api_model_name`` is the value sent as
``job_set_type`` on ``POST /internal/claudesfield/create-job`` — it differs
from the discriminator only for aliases (e.g. ``soul_v2`` → ``text2image_soul_v2``).
"""

from __future__ import annotations

import random
from typing import Any, Callable

from .client import HiggsfieldClient
from .media import (
    resolve_image_inputs,
    resolve_media_inputs,
    resolve_optional_image,
)

# ---------------------------------------------------------------------------
# Helpers (mirror generation/validate.go + defaulting patterns)
# ---------------------------------------------------------------------------


def _str(val: Any) -> str:
    if val is None:
        return ""
    return str(val)


def _default_str(val: Any, fallback: str) -> str:
    v = _str(val)
    return v if v else fallback


def _default_int(val: Any, fallback: int) -> int:
    try:
        n = int(val) if val is not None else 0
    except (TypeError, ValueError):
        n = 0
    return n if n != 0 else fallback


def _int_or_zero(val: Any) -> int:
    try:
        return int(val) if val is not None else 0
    except (TypeError, ValueError):
        return 0


def _default_bool(val: Any, fallback: bool) -> bool:
    if val is None:
        return fallback
    return bool(val)


def _default_float(val: Any, fallback: float) -> float:
    if val is None:
        return fallback
    try:
        return float(val)
    except (TypeError, ValueError):
        return fallback


def _random_seed(upper: int = 999999) -> int:
    return random.randint(1, upper)


def _validate_one_of(name: str, value: str, allowed: list[str]) -> None:
    if value not in allowed:
        raise ValueError(
            f"{name}: invalid value {value!r} (allowed: {', '.join(allowed)})"
        )


def _validate_int_range(name: str, value: int, lo: int, hi: int) -> None:
    if value < lo or value > hi:
        raise ValueError(f"{name}: value {value} out of range [{lo}, {hi}]")


def _validate_max_len(name: str, length: int, max_len: int) -> None:
    if length > max_len:
        raise ValueError(f"{name}: too many items ({length}), maximum is {max_len}")


def _validate_positive_int(name: str, value: int) -> None:
    if value < 1:
        raise ValueError(f"{name}: must be >= 1, got {value}")


def _validate_int_one_of(name: str, value: int, allowed: list[int]) -> None:
    if value not in allowed:
        allowed_str = ", ".join(str(v) for v in allowed)
        raise ValueError(f"{name}: invalid value {value} (allowed: {allowed_str})")


def _folder_id(inp_folder: Any, cfg_folder: str) -> str:
    iv = _str(inp_folder)
    return iv if iv else cfg_folder


def _lookup_dim(
    table: dict[str, tuple[int, int]],
    aspect_ratio: str,
    default_wh: tuple[int, int],
) -> tuple[int, int]:
    return table.get(aspect_ratio, default_wh)


# ---------------------------------------------------------------------------
# Dimension tables (copied verbatim from the Go)
# ---------------------------------------------------------------------------

_IMAGEGEN2_DIMS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "3:2": (1024, 680),
    "2:3": (680, 1024),
}

_SOUL_V2_DIMS: dict[str, tuple[int, int]] = {
    "9:16": (1152, 2048),
    "3:4": (1536, 2048),
    "2:3": (1344, 2016),
    "1:1": (2048, 2048),
    "4:3": (2048, 1536),
    "16:9": (2048, 1152),
    "3:2": (2016, 1344),
}

_SOUL_CINEMATIC_DIMS: dict[str, tuple[int, int]] = {
    "9:16": (1152, 2048),
    "3:4": (1536, 2048),
    "2:3": (1344, 2016),
    "1:1": (2048, 2048),
    "4:3": (2048, 1536),
    "16:9": (2048, 1152),
    "3:2": (2016, 1344),
    "21:9": (2528, 1088),
}

_SEEDREAM_V5_LITE_DIMS: dict[str, dict[str, tuple[int, int]]] = {
    "basic": {
        "1:1": (2048, 2048),
        "4:3": (2304, 1728),
        "3:4": (1728, 2304),
        "16:9": (2848, 1600),
        "9:16": (1600, 2848),
        "3:2": (2496, 1664),
        "2:3": (1664, 2496),
        "21:9": (3136, 1344),
    },
    "high": {
        "1:1": (3072, 3072),
        "4:3": (3456, 2592),
        "3:4": (2592, 3456),
        "16:9": (4096, 2304),
        "9:16": (2304, 4096),
        "3:2": (3744, 2496),
        "2:3": (2496, 3744),
        "21:9": (4704, 2016),
    },
}

_IMAGE_AUTO_DIMS: dict[str, tuple[int, int]] = {
    "1:1": (2048, 2048),
    "4:3": (2048, 1536),
    "3:4": (1536, 2048),
    "16:9": (2048, 1152),
    "9:16": (1152, 2048),
    "2:3": (1536, 2304),
    "3:2": (2304, 1536),
    "21:9": (2520, 1080),
}

_FLUX_2_DIMS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "3:2": (1200, 800),
    "2:3": (800, 1200),
}

_OPENAI_HAZEL_DIMS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "3:2": (1024, 680),
    "2:3": (680, 1024),
    "auto": (1024, 1024),
}

_KLING_OMNI_IMAGE_DIMS: dict[str, tuple[int, int]] = {
    "auto": (1024, 1024),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "1:1": (1024, 1024),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "3:2": (1200, 800),
    "2:3": (800, 1200),
    "21:9": (1344, 576),
}

_GROK_IMAGE_DIMS: dict[str, tuple[int, int]] = {
    "auto": (1024, 1024),
    "1:1": (1024, 1024),
    "1:2": (512, 1024),
    "2:1": (1024, 512),
    "3:2": (1200, 800),
    "2:3": (800, 1200),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
}

_Z_IMAGE_DIMS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
}

_SEEDANCE_DIMS: dict[str, tuple[int, int]] = {
    "21:9": (1344, 576),
    "16:9": (1280, 720),
    "4:3": (960, 720),
    "1:1": (720, 720),
    "3:4": (540, 720),
    "9:16": (720, 1280),
}

_SEEDANCE_15_DIMS: dict[str, tuple[int, int]] = {
    "auto": (1280, 720),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "4:3": (960, 720),
    "3:4": (540, 720),
    "1:1": (720, 720),
    "21:9": (1344, 576),
}

_KLING3_DIMS: dict[str, tuple[int, int]] = {
    "16:9": (1280, 720),
    "1:1": (720, 720),
    "9:16": (720, 1280),
}

_KLING26_DIMS: dict[str, tuple[int, int]] = {
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "1:1": (720, 720),
}

_CINEMATIC_STUDIO_25_DIMS: dict[str, tuple[int, int]] = {
    "1:1": (1024, 1024),
    "3:2": (1200, 800),
    "2:3": (800, 1200),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "4:5": (960, 1200),
    "5:4": (1200, 960),
    "9:16": (720, 1280),
    "16:9": (1280, 720),
    "21:9": (1344, 576),
}

_CINEMATIC_STUDIO_30_DIMS: dict[str, tuple[int, int]] = {
    "auto": (1280, 720),
    "21:9": (1344, 576),
    "16:9": (1280, 720),
    "4:3": (960, 720),
    "1:1": (720, 720),
    "3:4": (540, 720),
    "9:16": (720, 1280),
}

_MINIMAX_DIMS: dict[str, dict[str, tuple[int, int]]] = {
    "512": {
        "16:9": (910, 512),
        "9:16": (512, 910),
        "1:1": (512, 512),
    },
    "768": {
        "16:9": (1360, 768),
        "9:16": (768, 1360),
        "1:1": (768, 768),
    },
    "1080": {
        "16:9": (1920, 1080),
        "9:16": (1080, 1920),
        "1:1": (1080, 1080),
    },
}

_WAN26_DIMS: dict[str, tuple[int, int]] = {
    "4:3": (960, 720),
    "3:4": (540, 720),
    "1:1": (720, 720),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
}

_WAN27_DIMS: dict[str, tuple[int, int]] = {
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "1:1": (720, 720),
    "4:3": (960, 720),
    "3:4": (540, 720),
}

_VEO31_DIMS: dict[str, tuple[int, int]] = {
    "16:9": (1280, 720),
    "9:16": (720, 1280),
}

_VEO31_LITE_DIMS: dict[str, tuple[int, int]] = {
    "auto": (1280, 720),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
}

_GROK_VIDEO_DIMS: dict[str, tuple[int, int]] = {
    "auto": (1280, 720),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "4:3": (960, 720),
    "3:4": (540, 720),
    "1:1": (720, 720),
    "3:2": (1080, 720),
    "2:3": (480, 720),
}

# Enum tables ---------------------------------------------------------------

_IMAGEGEN2_ASPECTS = ["1:1", "3:2", "2:3", "auto"]
_IMAGEGEN2_QUALITIES = ["low", "medium", "high"]
_IMAGEGEN2_RESOLUTIONS = ["1k", "2k", "4k"]
_IMAGEGEN2_SUB_MODELS = [
    "cassettetape-alpha",
    "videotape-alpha",
    "electricaltape-alpha",
    "tidepool-alpha",
]

_NANO_BANANA_2_ASPECTS = [
    "auto", "1:1", "3:2", "2:3", "4:3", "3:4", "4:5", "5:4", "9:16", "16:9", "21:9",
]
_NANO_BANANA_2_RESOLUTIONS = ["1k", "2k", "4k"]

_SEEDREAM_ASPECTS = ["1:1", "4:3", "16:9", "3:2", "21:9", "3:4", "9:16", "2:3"]
_SEEDREAM_QUALITIES = ["basic", "high"]

_SOUL_CAST_GENRES = [
    "Action", "Adventure", "Comedy", "Drama", "Thriller", "Horror", "Detective",
    "Romance", "Sci-Fi", "Fantasy", "War", "Western", "Historical", "Sitcom",
]
_SOUL_CAST_GENDERS = ["male", "female"]
_SOUL_CAST_BUILDS = ["Slim", "Average", "Athletic", "Muscular", "Stocky", "Plus-size"]
_SOUL_CAST_HEIGHTS = ["Very short", "Short", "Average", "Tall", "Very tall"]
_SOUL_CAST_RACES = ["White", "Black", "Asian", "Latino", "Indigenous", "Mixed"]
_SOUL_CAST_HAIR_STYLES = [
    "Short", "Medium", "Long", "Very long", "Ponytail", "Bun", "Braids",
    "Dreadlocks", "Afro", "Fringe/Bangs", "Undercut", "Slick back", "Messy",
    "Shaved sides", "Bald",
]
_SOUL_CAST_HAIR_TEXTURES = ["Straight", "Wavy", "Curly", "Coily"]
_SOUL_CAST_FACIAL_HAIRS = [
    "Clean-shaven", "Stubble", "Beard", "Mustache", "Short beard", "Long beard",
]
_SOUL_CAST_ARCHETYPES = [
    "Innocent", "Everyman", "Hero", "Caregiver", "Explorer", "Rebel", "Lover",
    "Creator", "Jester", "Sage", "Magician", "Ruler",
]
_SOUL_CAST_BUDGETS = [
    10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
    150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500,
]


# ===========================================================================
# IMAGE MODELS
# ===========================================================================


def _build_imagegen_2_0(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "imagegen_2_0", inp.get("medias"))

    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _str(inp.get("aspect_ratio"))
    if not aspect_ratio:
        raise ValueError("aspect_ratio is required")
    _validate_one_of("aspect_ratio", aspect_ratio, _IMAGEGEN2_ASPECTS)

    quality = _default_str(inp.get("quality"), "low")
    _validate_one_of("quality", quality, _IMAGEGEN2_QUALITIES)

    resolution = _default_str(inp.get("resolution"), "1k")
    _validate_one_of("resolution", resolution, _IMAGEGEN2_RESOLUTIONS)

    sub_model = _default_str(inp.get("sub_model"), "videotape-alpha")
    _validate_one_of("sub_model", sub_model, _IMAGEGEN2_SUB_MODELS)

    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("medias", len(medias), 16)

    width, height = _lookup_dim(_IMAGEGEN2_DIMS, aspect_ratio, (1024, 1024))
    if _int_or_zero(inp.get("width")) > 0:
        width = int(inp["width"])
    if _int_or_zero(inp.get("height")) > 0:
        height = int(inp["height"])

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "quality": quality,
        "resolution": resolution,
        "sub_model": sub_model,
        "medias": medias,
        "aspect_ratio": aspect_ratio,
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_nano_banana_2(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    images = resolve_image_inputs(client, inp.get("images"))

    prompt = _str(inp.get("prompt"))
    if not prompt and not images:
        raise ValueError("either prompt or images is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    if aspect_ratio == "auto" and not images:
        raise ValueError("images is required when aspect_ratio is \"auto\"")
    _validate_one_of("aspect_ratio", aspect_ratio, _NANO_BANANA_2_ASPECTS)

    resolution = _default_str(inp.get("resolution"), "2k")
    _validate_one_of("resolution", resolution, _NANO_BANANA_2_RESOLUTIONS)

    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("images", len(images), 14)

    width = _default_int(inp.get("width"), 896)
    height = _default_int(inp.get("height"), 1200)
    _validate_positive_int("width", width)
    _validate_positive_int("height", height)

    return {
        "prompt": prompt,
        "input_images": images,
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "aspect_ratio": aspect_ratio,
        "is_storyboard": False,
        "is_zoom_control": False,
        "use_unlim": False,
        "resolution": resolution,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_nano_banana(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    images = resolve_image_inputs(client, inp.get("images"))
    prompt = _str(inp.get("prompt"))
    if not prompt and not images:
        raise ValueError("either prompt or images is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("images", len(images), 8)

    return {
        "prompt": prompt,
        "width": 896,
        "height": 1200,
        "input_images": images,
        "aspect_ratio": aspect_ratio,
        "is_draw": _default_bool(inp.get("is_draw"), False),
        "is_ugc": _default_bool(inp.get("is_ugc"), False),
        "is_product_placement": _default_bool(inp.get("is_product_placement"), False),
        "is_photo_set": _default_bool(inp.get("is_photo_set"), False),
        "fashion_factory_id": _str(inp.get("fashion_factory_id")),
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_flux_2(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    images = resolve_image_inputs(client, inp.get("images"))

    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    sub_model = _default_str(inp.get("sub_model"), "pro")
    aspect_ratio = _default_str(inp.get("aspect_ratio"), "1:1")
    width, height = _lookup_dim(_FLUX_2_DIMS, aspect_ratio, (1024, 1024))
    resolution = _default_str(inp.get("resolution"), "1k")

    batch_size = _default_int(inp.get("batch_size"), 2)
    _validate_int_range("batch_size", batch_size, 1, 4)

    seed = _default_int(inp.get("seed"), _random_seed())

    max_images = 8 if sub_model in {"pro", "max"} else 10
    _validate_max_len("images", len(images), max_images)

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "input_images": images,
        "seed": seed,
        "aspect_ratio": aspect_ratio,
        "model": sub_model,
        "resolution": resolution,
        "batch_size": batch_size,
        "steps": _int_or_zero(inp.get("steps")),
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if inp.get("cfg") is not None:
        params["cfg"] = float(inp["cfg"])
    return params


def _build_openai_hazel(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    images = resolve_image_inputs(client, inp.get("images"))
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "1:1")
    width, height = _lookup_dim(_OPENAI_HAZEL_DIMS, aspect_ratio, (1024, 1024))

    quality = _default_str(inp.get("quality"), "low")
    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("images", len(images), 16)

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "input_images": images,
        "aspect_ratio": aspect_ratio,
        "batch_size": batch_size,
        "quality": quality,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_kling_omni_image(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    images = resolve_image_inputs(client, inp.get("images"))
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "1:1")
    width, height = _lookup_dim(_KLING_OMNI_IMAGE_DIMS, aspect_ratio, (1024, 1024))
    resolution = _default_str(inp.get("resolution"), "1k")
    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("images", len(images), 10)

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "input_images": images,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_grok_image(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "grok_image", inp.get("medias"))
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    width, height = _lookup_dim(_GROK_IMAGE_DIMS, aspect_ratio, (1024, 1024))
    resolution = _default_str(inp.get("resolution"), "1k")
    mode = _default_str(inp.get("mode"), "std")

    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("medias", len(medias), 10)

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "medias": medias,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "mode": mode,
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_z_image(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    del client  # no media resolution for z_image
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "1:1")
    width, height = _lookup_dim(_Z_IMAGE_DIMS, aspect_ratio, (1024, 1024))
    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_image_auto(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "image_auto", inp.get("medias"))

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "1:1")
    width, height = _lookup_dim(_IMAGE_AUTO_DIMS, aspect_ratio, (2048, 2048))
    resolution = _default_str(inp.get("resolution"), "2k")
    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)

    return {
        "prompt": _str(inp.get("prompt")),
        "medias": medias,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


# ===========================================================================
# SOUL family
# ===========================================================================


def _build_soul_v2(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "text2image_soul_v2", inp.get("medias"))
    prompt = _str(inp.get("prompt"))
    if medias:
        prompt = ""
    elif not prompt:
        raise ValueError("prompt is required when no medias are provided")

    seed = _default_int(inp.get("seed"), _random_seed())
    style_id = _default_str(inp.get("style_id"), "3db34ab5-3439-4317-9e03-08dc30852e69")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "3:4")
    width, height = _lookup_dim(_SOUL_V2_DIMS, aspect_ratio, (1536, 2048))

    quality = _default_str(inp.get("quality"), "1080p")
    batch_size = _default_int(inp.get("batch_size"), 1)
    style_strength = _default_float(inp.get("style_strength"), 1.0)
    soul_strength = _default_float(inp.get("soul_strength"), 1.0)
    model_version = _default_str(inp.get("model_version"), "fast")
    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "seed": seed,
        "enhance_prompt": enhance_prompt,
        "quality": quality,
        "aspect_ratio": aspect_ratio,
        "medias": medias,
        "style_id": style_id,
        "style_strength": style_strength,
        "negative_prompt": _str(inp.get("negative_prompt")),
        "use_refiner": False,
        "use_green": True,
        "model_version": model_version,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if _str(inp.get("soul_id")):
        params["custom_reference_id"] = _str(inp.get("soul_id"))
        params["custom_reference_strength"] = soul_strength
    return params


def _build_soul_cinematic(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "soul_cinematic", inp.get("medias"))
    prompt = _str(inp.get("prompt"))
    if medias:
        prompt = ""
    elif not prompt:
        raise ValueError("prompt is required when no medias are provided")

    seed = _default_int(inp.get("seed"), _random_seed())
    style_id = _default_str(inp.get("style_id"), "5fbabfac-d27b-4751-b550-fea356ed55ac")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "16:9")
    width, height = _lookup_dim(_SOUL_CINEMATIC_DIMS, aspect_ratio, (2048, 1152))

    quality = _default_str(inp.get("quality"), "1080p")
    batch_size = _default_int(inp.get("batch_size"), 1)
    style_strength = _default_float(inp.get("style_strength"), 1.0)
    model_version = _default_str(inp.get("model_version"), "fast")
    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "seed": seed,
        "enhance_prompt": enhance_prompt,
        "quality": quality,
        "aspect_ratio": aspect_ratio,
        "medias": medias,
        "style_id": style_id,
        "style_strength": style_strength,
        "negative_prompt": _str(inp.get("negative_prompt")),
        "model_version": model_version,
        "use_sultan": True,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if medias:
        params["time_denoise_from"] = [0.83]
    return params


def _build_soul_cast(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    del client  # no media resolution for soul_cast
    width = _int_or_zero(inp.get("width"))
    height = _int_or_zero(inp.get("height"))
    _validate_positive_int("width", width)
    _validate_positive_int("height", height)

    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 10)

    raw_seed = _int_or_zero(inp.get("seed"))
    if raw_seed != 0:
        _validate_int_range("seed", raw_seed, 1, 1000000)
        seed = raw_seed
    else:
        seed = _random_seed()

    cp = inp.get("character_params") or {}
    if not isinstance(cp, dict):
        raise ValueError("character_params: must be an object")

    def _opt_one_of(field: str, values: list[str]) -> None:
        v = _str(cp.get(field))
        if v:
            _validate_one_of(field, v, values)

    _opt_one_of("genre", _SOUL_CAST_GENRES)
    _opt_one_of("gender", _SOUL_CAST_GENDERS)
    _opt_one_of("build", _SOUL_CAST_BUILDS)
    _opt_one_of("height", _SOUL_CAST_HEIGHTS)
    _opt_one_of("race", _SOUL_CAST_RACES)
    _opt_one_of("hair_style", _SOUL_CAST_HAIR_STYLES)
    _opt_one_of("hair_texture", _SOUL_CAST_HAIR_TEXTURES)
    _opt_one_of("facial_hair", _SOUL_CAST_FACIAL_HAIRS)
    _opt_one_of("archetype", _SOUL_CAST_ARCHETYPES)
    if len(_str(cp.get("eye_color"))) > 100:
        raise ValueError("eye_color: max 100 characters")
    if len(_str(cp.get("hair_color"))) > 100:
        raise ValueError("hair_color: max 100 characters")
    if len(_str(cp.get("imperfections"))) > 300:
        raise ValueError("imperfections: max 300 characters")
    if len(_str(cp.get("outfit"))) > 300:
        raise ValueError("outfit: max 300 characters")

    budget = _int_or_zero(cp.get("budget"))
    _validate_int_one_of("budget", budget, _SOUL_CAST_BUDGETS)

    character_params: dict[str, Any] = {"budget": budget}
    for field in (
        "genre", "era", "gender", "build", "height", "race", "eye_color",
        "hair_style", "hair_texture", "hair_color", "facial_hair", "age",
        "archetype", "imperfections", "outfit",
    ):
        val = _str(cp.get(field))
        if val:
            character_params[field] = val

    params: dict[str, Any] = {
        "prompt": _str(inp.get("prompt")),
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "seed": seed,
        "character_params": character_params,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if _str(inp.get("style_id")):
        params["style_id"] = _str(inp.get("style_id"))
    if _str(inp.get("preset_id")):
        params["preset_id"] = _str(inp.get("preset_id"))
    return params


def _build_soul_location(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    del client  # no media resolution for soul_location
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    width = _int_or_zero(inp.get("width"))
    height = _int_or_zero(inp.get("height"))
    _validate_positive_int("width", width)
    _validate_positive_int("height", height)

    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 10)

    seed = _default_int(inp.get("seed"), _random_seed())

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "seed": seed,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


# ===========================================================================
# SEEDREAM family
# ===========================================================================


def _build_seedream_v5_lite(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "seedream_v5_lite", inp.get("medias"))

    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _str(inp.get("aspect_ratio"))
    if not aspect_ratio:
        raise ValueError("aspect_ratio is required")
    _validate_one_of("aspect_ratio", aspect_ratio, _SEEDREAM_ASPECTS)

    quality = _str(inp.get("quality"))
    if not quality:
        raise ValueError("quality is required")
    _validate_one_of("quality", quality, _SEEDREAM_QUALITIES)

    batch_size = _default_int(inp.get("batch_size"), 4)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("medias", len(medias), 14)

    seed = _default_int(inp.get("seed"), _random_seed())

    width, height = _lookup_dim(_SEEDREAM_V5_LITE_DIMS.get(quality, {}), aspect_ratio, (1024, 1024))

    return {
        "prompt": prompt,
        "medias": medias,
        "width": width,
        "height": height,
        "quality": quality,
        "batch_size": batch_size,
        "aspect_ratio": aspect_ratio,
        "seed": seed,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_seedream_v4_5(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    images = resolve_image_inputs(client, inp.get("images"))

    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _str(inp.get("aspect_ratio"))
    if not aspect_ratio:
        raise ValueError("aspect_ratio is required")
    _validate_one_of("aspect_ratio", aspect_ratio, _SEEDREAM_ASPECTS)

    quality = _default_str(inp.get("quality"), "basic")
    _validate_one_of("quality", quality, _SEEDREAM_QUALITIES)

    batch_size = _default_int(inp.get("batch_size"), 4)
    _validate_int_range("batch_size", batch_size, 1, 4)
    _validate_max_len("images", len(images), 14)

    seed = _default_int(inp.get("seed"), _random_seed())

    return {
        "prompt": prompt,
        "input_images": images,
        "quality": quality,
        "aspect_ratio": aspect_ratio,
        "seed": seed,
        "batch_size": batch_size,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


# ===========================================================================
# VIDEO family
# ===========================================================================


def _build_seedance_2_0(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    medias = resolve_media_inputs(client, "seedance_2_0", inp.get("medias"))

    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "1:1")
    width, height = _lookup_dim(_SEEDANCE_DIMS, aspect_ratio, (720, 720))
    duration = _default_int(inp.get("duration"), 8)
    resolution = _default_str(inp.get("resolution"), "720p")
    use_eye_mask = _default_bool(inp.get("use_eye_mask"), False)

    return {
        "prompt": prompt,
        "medias": medias,
        "duration": duration,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "generate_audio": True,
        "use_transparency": False,
        "use_eye_mask": use_eye_mask,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_seedance_1_5(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    medias = resolve_media_inputs(client, "seedance1_5", inp.get("medias"))
    _validate_max_len("medias", len(medias), 2)

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    width, height = _lookup_dim(_SEEDANCE_15_DIMS, aspect_ratio, (1280, 720))

    duration = _default_int(inp.get("duration"), 4)
    resolution = _default_str(inp.get("resolution"), "720p")
    fixed_lens = _default_bool(inp.get("fixed_lens"), False)
    generate_audio = _default_bool(inp.get("generate_audio"), True)

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "medias": medias,
        "duration": duration,
        "fixed_lens": fixed_lens,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "seed": _int_or_zero(inp.get("seed")),
        "generate_audio": generate_audio,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_kling3_0(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "16:9")
    if aspect_ratio not in _KLING3_DIMS:
        raise ValueError(
            f"aspect_ratio: invalid value {aspect_ratio!r} (allowed: 16:9, 9:16, 1:1)"
        )

    width = _int_or_zero(inp.get("width"))
    height = _int_or_zero(inp.get("height"))
    if width == 0 or height == 0:
        width, height = _KLING3_DIMS[aspect_ratio]

    mode = _default_str(inp.get("mode"), "std")
    if mode not in {"std", "pro"}:
        raise ValueError(f"mode: invalid value {mode!r} (allowed: pro, std)")

    duration = _default_int(inp.get("duration"), 5)
    if duration < 3 or duration > 15:
        raise ValueError(f"duration: value {duration} out of range [3, 15]")

    medias = resolve_media_inputs(client, "kling3_0", inp.get("medias"))

    sound = _default_str(inp.get("sound"), "on")
    cfg_scale = _default_float(inp.get("cfg_scale"), 0.5)
    multi_shots = _default_bool(inp.get("multi_shots"), False)
    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)
    multi_shot_mode = _default_str(inp.get("multi_shot_mode"), "custom")
    multi_prompt = inp.get("multi_prompt") or []
    kling_element_ids = inp.get("kling_element_ids") or []

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "mode": mode,
        "duration": duration,
        "medias": medias,
        "multi_shots": multi_shots,
        "multi_prompt": list(multi_prompt),
        "sound": sound,
        "cfg_scale": cfg_scale,
        "kling_element_ids": list(kling_element_ids),
        "multi_shot_mode": multi_shot_mode,
        "enhance_prompt": enhance_prompt,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_kling_2_6(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    duration = _default_int(inp.get("duration"), 5)

    aspect_ratio = _str(inp.get("aspect_ratio"))
    width, height = (1280, 720)
    if aspect_ratio and aspect_ratio in _KLING26_DIMS:
        width, height = _KLING26_DIMS[aspect_ratio]

    cfg_scale = _default_float(inp.get("cfg_scale"), 0.5)
    sound = _default_bool(inp.get("sound"), True)

    input_image = resolve_optional_image(client, inp.get("input_image"))

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "cfg_scale": cfg_scale,
        "sound": sound,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if input_image is not None:
        params["input_image"] = input_image
    if _str(inp.get("negative_prompt")):
        params["negative_prompt"] = _str(inp.get("negative_prompt"))
    if _str(inp.get("motion_id")):
        params["motion_id"] = _str(inp.get("motion_id"))
    return params


def _build_cinematic_studio_2_5(
    inp: dict, *, client: HiggsfieldClient, folder_id: str
) -> dict:
    medias = resolve_media_inputs(client, "cinematic_studio_2_5", inp.get("medias"))
    _validate_max_len("medias", len(medias), 14)

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "21:9")
    width, height = _lookup_dim(_CINEMATIC_STUDIO_25_DIMS, aspect_ratio, (1024, 1024))

    mode = _default_str(inp.get("mode"), "auto")
    resolution = _default_str(inp.get("resolution"), "2k")

    batch_size = _default_int(inp.get("batch_size"), 1)
    _validate_int_range("batch_size", batch_size, 1, 4)

    return {
        "prompt": _str(inp.get("prompt")),
        "medias": medias,
        "mode": mode,
        "seed": _int_or_zero(inp.get("seed")),
        "width": width,
        "height": height,
        "batch_size": batch_size,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_cinematic_studio_3_0(
    inp: dict, *, client: HiggsfieldClient, folder_id: str
) -> dict:
    medias = resolve_media_inputs(client, "cinematic_studio_3_0", inp.get("medias"))
    _validate_max_len("medias", len(medias), 15)

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    width, height = _lookup_dim(_CINEMATIC_STUDIO_30_DIMS, aspect_ratio, (1280, 720))

    genre = _default_str(inp.get("genre"), "auto")
    duration = _default_int(inp.get("duration"), 15)
    resolution = _default_str(inp.get("resolution"), "720p")
    batch_size = _default_int(inp.get("batch_size"), 1)

    multi_shots = _default_bool(inp.get("multi_shots"), False)
    speedramp = _default_bool(inp.get("speedramp"), False)
    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)
    multi_prompt = inp.get("multi_prompt") or []

    params: dict[str, Any] = {
        "prompt": _str(inp.get("prompt")),
        "width": width,
        "height": height,
        "genre": genre,
        "medias": medias,
        "duration": duration,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "generate_audio": True,
        "multi_shots": multi_shots,
        "multi_prompt": list(multi_prompt),
        "speedramp": speedramp,
        "batch_size": batch_size,
        "enhance_prompt": enhance_prompt,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if _str(inp.get("multi_shot_mode")):
        params["multi_shot_mode"] = _str(inp.get("multi_shot_mode"))
    if _str(inp.get("preset_id")):
        params["preset_id"] = _str(inp.get("preset_id"))
    return params


def _build_minimax_hailuo(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    sub_model = _default_str(inp.get("sub_model"), "minimax")
    duration = _default_int(inp.get("duration"), 6)
    resolution = _default_str(inp.get("resolution"), "768")
    aspect_ratio = _default_str(inp.get("aspect_ratio"), "16:9")

    width, height = (1360, 768)
    res_map = _MINIMAX_DIMS.get(resolution)
    if res_map is not None:
        width, height = res_map.get(aspect_ratio, (width, height))

    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)
    is_draw = _default_bool(inp.get("is_draw"), False)

    input_image = resolve_optional_image(client, inp.get("input_image"))
    input_image_end = resolve_optional_image(client, inp.get("input_image_end"))
    draw_input_image = resolve_optional_image(client, inp.get("draw_input_image"))

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": sub_model,
        "enhance_prompt": enhance_prompt,
        "duration": duration,
        "resolution": resolution,
        "is_draw": is_draw,
        "seed": _int_or_zero(inp.get("seed")),
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if input_image is not None:
        params["input_image"] = input_image
    if input_image_end is not None:
        params["input_image_end"] = input_image_end
    if draw_input_image is not None:
        params["draw_input_image"] = draw_input_image
    if _str(inp.get("motion_id")):
        params["motion_id"] = _str(inp.get("motion_id"))
    return params


def _build_wan_2_6(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    images = resolve_image_inputs(client, inp.get("images"))
    _validate_max_len("images", len(images), 1)

    input_videos = resolve_image_inputs(client, inp.get("input_videos"))
    _validate_max_len("input_videos", len(input_videos), 3)

    input_audio = resolve_optional_image(client, inp.get("input_audio"))

    seed = _default_int(inp.get("seed"), random.randint(1, 10000000))
    duration = _default_int(inp.get("duration"), 5)
    quality = _default_str(inp.get("quality"), "720p")
    multi_shots = _default_bool(inp.get("multi_shots"), False)

    aspect_ratio = _str(inp.get("aspect_ratio"))
    width, height = (1280, 720)
    if aspect_ratio and aspect_ratio in _WAN26_DIMS:
        width, height = _WAN26_DIMS[aspect_ratio]

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "seed": seed,
        "duration": duration,
        "input_images": images,
        "quality": quality,
        "multi_shots": multi_shots,
        "aspect_ratio": aspect_ratio,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if input_audio is not None:
        params["input_audio"] = input_audio
    if input_videos:
        params["input_videos"] = input_videos
    if _str(inp.get("negative_prompt")):
        params["negative_prompt"] = _str(inp.get("negative_prompt"))
    return params


def _build_wan_2_7(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    medias = resolve_media_inputs(client, "wan2_7", inp.get("medias"))

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "16:9")
    width, height = _lookup_dim(_WAN27_DIMS, aspect_ratio, (1280, 720))

    duration = _default_int(inp.get("duration"), 5)
    resolution = _default_str(inp.get("resolution"), "720p")

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "medias": medias,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "seed": _int_or_zero(inp.get("seed")),
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_veo3(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "16:9")
    seed = _default_int(inp.get("seed"), _random_seed())
    quality = _default_str(inp.get("quality"), "basic")
    sub_model = _default_str(inp.get("sub_model"), "veo-3-fast")

    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)
    is_draw = _default_bool(inp.get("is_draw"), False)

    if inp.get("input_image") is None:
        raise ValueError("input_image is required for veo3")
    input_image = resolve_optional_image(client, inp.get("input_image"))
    draw_input_image = resolve_optional_image(client, inp.get("draw_input_image"))

    params: dict[str, Any] = {
        "prompt": prompt,
        "input_image": input_image,
        "enhance_prompt": enhance_prompt,
        "seed": seed,
        "aspect_ratio": aspect_ratio,
        "model": sub_model,
        "quality": quality,
        "is_draw": is_draw,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if draw_input_image is not None:
        params["draw_input_image"] = draw_input_image
    if _str(inp.get("motion_id")):
        params["motion_id"] = _str(inp.get("motion_id"))
    return params


def _build_veo3_1(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "16:9")
    width, height = _lookup_dim(_VEO31_DIMS, aspect_ratio, (1280, 720))

    seed = _default_int(inp.get("seed"), _random_seed())
    duration = _default_int(inp.get("duration"), 8)
    sub_model = _default_str(inp.get("sub_model"), "veo-3-1-fast")
    quality = _default_str(inp.get("quality"), "basic")

    enhance_prompt = _default_bool(inp.get("enhance_prompt"), False)
    generate_audio = _default_bool(inp.get("generate_audio"), True)
    is_draw = _default_bool(inp.get("is_draw"), False)
    scene_cut = _default_bool(inp.get("scene_cut"), False)

    input_image = resolve_optional_image(client, inp.get("input_image"))
    draw_input_image = resolve_optional_image(client, inp.get("draw_input_image"))
    end_input_image = resolve_optional_image(client, inp.get("end_input_image"))
    style_input_image = resolve_optional_image(client, inp.get("style_input_image"))

    ref_images = resolve_image_inputs(client, inp.get("reference_input_images"))
    _validate_max_len("reference_input_images", len(ref_images), 3)

    mode = _str(inp.get("mode"))
    if not mode:
        if ref_images:
            mode = "reference_images"
        elif style_input_image is not None:
            mode = "style_image"
        elif input_image is not None or draw_input_image is not None or end_input_image is not None:
            mode = "input_images"
        else:
            mode = "input_text"

    params: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "quality": quality,
        "aspect_ratio": aspect_ratio,
        "model": sub_model,
        "enhance_prompt": enhance_prompt,
        "seed": seed,
        "mode": mode,
        "duration": duration,
        "generate_audio": generate_audio,
        "is_draw": is_draw,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }
    if scene_cut:
        params["scene_cut"] = True
    if _str(inp.get("motion_id")):
        params["motion_id"] = _str(inp.get("motion_id"))
    if input_image is not None:
        params["input_image"] = input_image
    if draw_input_image is not None:
        params["draw_input_image"] = draw_input_image
    if end_input_image is not None:
        params["end_input_image"] = end_input_image
    if style_input_image is not None:
        params["style_input_image"] = style_input_image
    if ref_images:
        params["reference_input_images"] = ref_images
    return params


def _build_veo3_1_lite(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    medias = resolve_media_inputs(client, "veo3_1_lite", inp.get("medias"))
    _validate_max_len("medias", len(medias), 2)

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    width, height = _lookup_dim(_VEO31_LITE_DIMS, aspect_ratio, (1280, 720))

    duration = _default_int(inp.get("duration"), 8)
    resolution = _default_str(inp.get("resolution"), "720p")
    generate_audio = _default_bool(inp.get("generate_audio"), False)
    seed = _default_int(inp.get("seed"), random.randint(1, 2147483645))

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "medias": medias,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "generate_audio": generate_audio,
        "resolution": resolution,
        "seed": seed,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


def _build_grok_video(inp: dict, *, client: HiggsfieldClient, folder_id: str) -> dict:
    prompt = _str(inp.get("prompt"))
    if not prompt:
        raise ValueError("prompt is required")

    medias = resolve_media_inputs(client, "grok_video", inp.get("medias"))
    _validate_max_len("medias", len(medias), 1)

    aspect_ratio = _default_str(inp.get("aspect_ratio"), "auto")
    width, height = _lookup_dim(_GROK_VIDEO_DIMS, aspect_ratio, (1280, 720))

    duration = _default_int(inp.get("duration"), 5)
    resolution = _default_str(inp.get("resolution"), "720p")

    return {
        "prompt": prompt,
        "width": width,
        "height": height,
        "medias": medias,
        "duration": duration,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "folder_id": _folder_id(inp.get("folder_id"), folder_id),
        "tool_use_id": _str(inp.get("tool_use_id")),
    }


# ===========================================================================
# Dispatch table
# ===========================================================================

BuilderFn = Callable[..., dict]

# (input discriminator) -> (FNF job_set_type, builder fn)
BUILDERS: dict[str, tuple[str, BuilderFn]] = {
    # images
    "imagegen_2_0": ("imagegen_2_0", _build_imagegen_2_0),
    "nano_banana_2": ("nano_banana_2", _build_nano_banana_2),
    "nano_banana": ("nano_banana", _build_nano_banana),
    "flux_2": ("flux_2", _build_flux_2),
    "openai_hazel": ("openai_hazel", _build_openai_hazel),
    "kling_omni_image": ("kling_omni_image", _build_kling_omni_image),
    "grok_image": ("grok_image", _build_grok_image),
    "z_image": ("z_image", _build_z_image),
    "image_auto": ("image_auto", _build_image_auto),
    # soul family
    "soul_v2": ("text2image_soul_v2", _build_soul_v2),
    "text2image_soul_v2": ("text2image_soul_v2", _build_soul_v2),
    "soul_cinematic": ("soul_cinematic", _build_soul_cinematic),
    "soul_cast": ("soul_cast", _build_soul_cast),
    "soul_location": ("soul_location", _build_soul_location),
    # seedream family
    "seedream_v5_lite": ("seedream_v5_lite", _build_seedream_v5_lite),
    "seedream_v4_5": ("seedream_v4_5", _build_seedream_v4_5),
    # video
    "seedance_2_0": ("seedance_2_0", _build_seedance_2_0),
    "claudesfield_video": ("claudesfield_video", _build_seedance_2_0),
    "seedance1_5": ("seedance1_5", _build_seedance_1_5),
    "kling3_0": ("kling3_0", _build_kling3_0),
    "kling2_6": ("kling2_6", _build_kling_2_6),
    "cinematic_studio_2_5": ("cinematic_studio_2_5", _build_cinematic_studio_2_5),
    "cinematic_studio_3_0": ("cinematic_studio_3_0", _build_cinematic_studio_3_0),
    "minimax_hailuo": ("minimax_hailuo", _build_minimax_hailuo),
    "wan2_6": ("wan2_6", _build_wan_2_6),
    "wan2_7": ("wan2_7", _build_wan_2_7),
    "veo3": ("veo3", _build_veo3),
    "veo3_1": ("veo3_1", _build_veo3_1),
    "veo3_1_lite": ("veo3_1_lite", _build_veo3_1_lite),
    "grok_video": ("grok_video", _build_grok_video),
}


def supported_models() -> list[str]:
    return sorted(BUILDERS.keys())
