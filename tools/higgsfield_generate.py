"""higgsfield_generate — submit a Higgsfield FNF generation job, poll, return result.

Native Python port of ``higgsfieldcli generate --json``. Replaces the Go CLI
wrapper so no subprocess / binary is needed. Talks directly to
``FNF_BASE_URL`` via HTTP using the auth headers defined in
``higgsfieldcli/internal/api/client.go``.

Behavior:
- Blocks and polls until the job reaches a terminal status, then returns the
  result URL.
- Pass ``async=true`` to skip polling and return ``{job_set_id, job_ids,
  status: "created"}`` immediately.
- ``model`` is the discriminator; see ``tools/higgsfield/builders.py:BUILDERS``
  for the full list of supported values.
"""

from __future__ import annotations

import logging
from typing import Any

from tools.higgsfield.auth import (
    config_is_available,
    load_config,
    missing_env_vars,
)
from tools.higgsfield.builders import BUILDERS, supported_models
from tools.higgsfield.client import HiggsfieldClient
from tools.higgsfield.errors import (
    HiggsfieldAPIError,
    HiggsfieldConfigError,
    HiggsfieldError,
    HiggsfieldTimeout,
)
from tools.higgsfield.polling import terminal_result, wait_for_job
from tools.registry import registry, tool_error, tool_result

logger = logging.getLogger(__name__)


def _poll_all(
    client: HiggsfieldClient,
    job_ids: list[str],
    *,
    interval: float,
    timeout: float,
) -> list[dict]:
    results: list[dict] = []
    for jid in job_ids:
        try:
            status = wait_for_job(client, jid, interval=interval, timeout=timeout)
        except HiggsfieldTimeout as exc:
            results.append({"job_id": jid, "status": "timeout", "error": str(exc)})
            continue
        results.append(terminal_result(client, status))
    return results


def higgsfield_generate(args: dict, **_kw) -> str:
    model = args.get("model")
    if not model:
        return tool_error("\"model\" field is required")
    if model not in BUILDERS:
        return tool_error(
            f"unknown model {model!r}; supported: {', '.join(supported_models())}"
        )

    try:
        cfg = load_config()
    except HiggsfieldConfigError as exc:
        return tool_error(str(exc), missing_env=list(exc.missing))

    folder_id = args.get("folder_id") or cfg.folder_id
    async_submit = bool(args.get("async") or args.get("async_submit"))
    interval = float(args.get("poll_interval") or 5.0)
    timeout = float(args.get("timeout_seconds") or 900.0)

    job_set_type, builder = BUILDERS[model]

    try:
        with HiggsfieldClient(cfg) as client:
            try:
                params = builder(args, client=client, folder_id=folder_id)
            except ValueError as exc:
                return tool_error(f"{model}: {exc}")

            create_resp = client.create_job(job_set_type, params)

            if not isinstance(create_resp, dict) or not create_resp.get("job_sets"):
                return tool_error(
                    "unexpected create-job response",
                    raw=create_resp,
                )
            job_set = create_resp["job_sets"][0]
            job_ids = list(job_set.get("job_ids") or [])
            payload: dict[str, Any] = {
                "job_set_id": job_set.get("job_set_id", ""),
                "job_set_type": job_set.get("job_set_type", job_set_type),
                "job_ids": job_ids,
            }

            if async_submit:
                payload["status"] = "created"
                return tool_result(payload)

            # Block until each job reaches a terminal status.
            payload["jobs"] = _poll_all(
                client, job_ids, interval=interval, timeout=timeout
            )
            # Convenience fields when exactly one job.
            if len(payload["jobs"]) == 1:
                j = payload["jobs"][0]
                payload["status"] = j.get("status", "")
                if "result" in j:
                    payload["result"] = j["result"]
            return tool_result(payload)

    except HiggsfieldAPIError as exc:
        return tool_error(str(exc), status_code=exc.status_code, body=exc.body)
    except HiggsfieldError as exc:
        return tool_error(str(exc))
    except Exception as exc:  # pragma: no cover — defensive
        logger.exception("higgsfield_generate failed")
        return tool_error(f"unexpected error: {type(exc).__name__}: {exc}")


HIGGSFIELD_GENERATE_SCHEMA = {
    "name": "higgsfield_generate",
    "description": (
        "Submit a Higgsfield FNF generation job (image or video) and return the "
        "result URL. Blocks until the job finishes unless async=true. The "
        "'model' field picks which generator runs; each model has its own "
        "required/optional fields. Supported models: "
        + ", ".join(supported_models())
        + ". Media/image IDs must be pre-existing (upload flow is not exposed "
        "as a tool). Results come back as {job_set_id, job_set_type, job_ids, "
        "status, result?: {type, url}}."
    ),
    "parameters": {
        "type": "object",
        "required": ["model"],
        "properties": {
            "model": {
                "type": "string",
                "enum": supported_models(),
                "description": "Which generator to run. Routes to the model-specific request builder.",
            },
            "prompt": {
                "type": "string",
                "description": "Text prompt. Required for most models; image-to-image models ignore it when medias/images are provided.",
            },
            "aspect_ratio": {
                "type": "string",
                "description": "Aspect ratio (e.g. 1:1, 16:9). Model-dependent; some models require it.",
            },
            "quality": {"type": "string", "description": "Model-specific quality tier."},
            "resolution": {"type": "string", "description": "Model-specific resolution tier."},
            "batch_size": {"type": "integer", "description": "Number of images/videos to generate; range depends on model (commonly 1–4)."},
            "seed": {"type": "integer", "description": "Random seed; 0 or omit for random."},
            "duration": {"type": "integer", "description": "Duration in seconds (video models)."},
            "width": {"type": "integer", "description": "Override width; most models derive it from aspect_ratio."},
            "height": {"type": "integer", "description": "Override height; most models derive it from aspect_ratio."},
            "medias": {
                "type": "array",
                "description": "Input medias: [{role, data: {id, type?, url?}}]. Role defaults to 'image'.",
                "items": {
                    "type": "object",
                    "required": ["data"],
                    "properties": {
                        "role": {"type": "string"},
                        "data": {
                            "type": "object",
                            "required": ["id"],
                            "properties": {
                                "id": {"type": "string"},
                                "type": {"type": "string"},
                                "url": {"type": "string"},
                            },
                        },
                    },
                },
            },
            "images": {
                "type": "array",
                "description": "Input images for flat-list models: [{id, type?, url?}].",
                "items": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "url": {"type": "string"},
                    },
                },
            },
            "sub_model": {"type": "string", "description": "Sub-model selector (imagegen_2_0, flux_2, minimax_hailuo, veo3, veo3_1)."},
            "mode": {"type": "string", "description": "Mode selector for models that have one (kling3_0, cinematic_studio_2_5, veo3_1, grok_image, etc.)."},
            "style_id": {"type": "string", "description": "Style preset UUID (soul family)."},
            "style_strength": {"type": "number", "description": "Style strength 0.0–1.0 (soul family)."},
            "soul_id": {"type": "string", "description": "Custom Soul ID (soul_v2)."},
            "soul_strength": {"type": "number", "description": "Soul ID strength 0.0–1.0 (soul_v2)."},
            "negative_prompt": {"type": "string"},
            "enhance_prompt": {"type": "boolean"},
            "model_version": {"type": "string", "description": "soul_v2 / soul_cinematic: 'fast' (default)."},
            "character_params": {
                "type": "object",
                "description": "soul_cast character description. Most fields optional; budget is required (allowed values defined by the API).",
                "properties": {
                    "genre": {"type": "string"},
                    "era": {"type": "string"},
                    "gender": {"type": "string"},
                    "build": {"type": "string"},
                    "height": {"type": "string"},
                    "race": {"type": "string"},
                    "eye_color": {"type": "string"},
                    "hair_style": {"type": "string"},
                    "hair_texture": {"type": "string"},
                    "hair_color": {"type": "string"},
                    "facial_hair": {"type": "string"},
                    "age": {"type": "string"},
                    "archetype": {"type": "string"},
                    "imperfections": {"type": "string"},
                    "outfit": {"type": "string"},
                    "budget": {"type": "integer"},
                },
            },
            "preset_id": {"type": "string"},
            "generate_audio": {"type": "boolean", "description": "Enable audio track (video models that support it)."},
            "use_eye_mask": {"type": "boolean"},
            "fixed_lens": {"type": "boolean"},
            "sound": {
                "description": "kling3_0: 'on'/'off' string. kling2_6: boolean.",
            },
            "cfg_scale": {"type": "number"},
            "multi_shots": {"type": "boolean"},
            "multi_prompt": {"type": "array", "items": {"type": "string"}},
            "multi_shot_mode": {"type": "string"},
            "kling_element_ids": {"type": "array", "items": {"type": "string"}},
            "motion_id": {"type": "string"},
            "scene_cut": {"type": "boolean"},
            "genre": {"type": "string", "description": "cinematic_studio_3_0 genre override."},
            "speedramp": {"type": "boolean"},
            "steps": {"type": "integer", "description": "flux_2 sampler steps."},
            "cfg": {"type": "number", "description": "flux_2 cfg."},
            "is_draw": {"type": "boolean"},
            "is_ugc": {"type": "boolean"},
            "is_product_placement": {"type": "boolean"},
            "is_photo_set": {"type": "boolean"},
            "fashion_factory_id": {"type": "string"},
            "input_image": {
                "type": "object",
                "description": "Single optional image for veo3, kling2_6, minimax_hailuo, veo3_1.",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
            "input_image_end": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
            "draw_input_image": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
            "end_input_image": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
            "style_input_image": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
            "reference_input_images": {
                "type": "array",
                "description": "veo3_1 reference images.",
                "items": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "url": {"type": "string"},
                    },
                },
            },
            "input_audio": {
                "type": "object",
                "description": "wan2_6 input audio.",
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
            "input_videos": {
                "type": "array",
                "description": "wan2_6 input videos (up to 3).",
                "items": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "url": {"type": "string"},
                    },
                },
            },
            "folder_id": {"type": "string", "description": "Override HF_FOLDER_ID for this request."},
            "tool_use_id": {"type": "string", "description": "Correlation ID echoed back in results."},
            "async": {"type": "boolean", "description": "When true, return job IDs immediately without polling."},
            "poll_interval": {"type": "number", "description": "Seconds between status checks (default 5)."},
            "timeout_seconds": {"type": "number", "description": "Max wall-clock seconds to wait per job when polling (default 900)."},
        },
    },
}


def _check_higgsfield_available() -> bool:
    if not config_is_available():
        logger.debug("higgsfield toolset unavailable: %s", missing_env_vars())
        return False
    return True


registry.register(
    name="higgsfield_generate",
    toolset="higgsfield",
    schema=HIGGSFIELD_GENERATE_SCHEMA,
    handler=higgsfield_generate,
    check_fn=_check_higgsfield_available,
    requires_env=[
        "FNF_BASE_URL",
        "HF_FOLDER_ID",
        "HF_JWT_TOKEN (prod) or HF_DEV_USER_ID (dev)",
    ],
    description="Submit a Higgsfield FNF generation job and poll to completion.",
    emoji="🎨",
)
