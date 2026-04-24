# Port `higgsfieldcli generate` to native Python Hermes tools

**Source:** `/Users/arsenkipachu/Desktop/higgsfield/higgsfieldcli` (Go — being deprecated)
**Target:** Hermes `tools/` (Python) — talks directly to FNF over HTTP
**Scope:** `generate` only. Upload, balance, status-as-tool, soul-id, element, inspiration, cron, skill-publish, job-ip-check, connector are **out of scope**.

---

## 1. Goal

Replace the `higgsfieldcli generate` code path with a pure-Python implementation
exposed to the Hermes agent as tools. The Go binary gets deprecated; the
Python implementation talks to FNF (`FNF_BASE_URL`) over HTTP using the same
auth headers. No subprocess, no binary dependency.

---

## 2. What `generate` actually does (mapped from the Go)

### HTTP surface (from `internal/api/`)

- `POST /internal/claudesfield/create-job` body `{job_set_type: <model>, params: <model-specific>}` → `{job_sets: [{job_set_id, job_set_type, job_ids: [...]}]}`
- `GET  /internal/claudesfield/jobs/{id}/status` → `{id, status, ip_check_finished, ip_detected, job_set_type}`
- `GET  /internal/claudesfield/jobs/{id}` → `{id, status, job_set_type, job_set_id, params, result?, results?: {raw: {type, url}, min: {type, url}}}`
- `GET  /input-images/{id}` → `{id, type, url}` (used to enrich media items that arrive with only an `id`)

### Auth headers (from `internal/api/client.go:42`)
```
hf-dev-user-id:        <HF_DEV_USER_ID>     # dev
hf-dev-folder-id:      <HF_FOLDER_ID>       # always
X-Claudesfield-Token:  <HF_JWT_TOKEN>       # prod
Accept: application/json
Content-Type: application/json (on POSTs)
```
Note: the header is **`X-Claudesfield-Token`**, not `Authorization: Bearer`. `HF_INTERNAL_API_KEY` is declared in README but not actually attached by the Go client we read — confirm before porting.

### Flow per request
1. Parse input JSON; extract `model` (discriminator).
2. Per-model: apply defaults, validate enums/ranges, derive `width`/`height` from `aspect_ratio` (lookup table per model), resolve any media IDs via `GET /input-images/{id}` when `type`/`url` missing.
3. Build the model-specific params struct, call `POST /internal/claudesfield/create-job`.
4. For each `job_id` in the response: poll `GET /jobs/{id}/status` on an interval until status ∈ `{completed, canceled, failed, nsfw, ip_detected}`.
5. `GET /jobs/{id}` for the full result (`results.raw.url`, `results.min.url`).
6. Emit normalized JSON back to the agent.

### Models to support (discriminator values, from `generate.go:143`)

**Tier 1 — actively used by existing skills (ship first):**
`imagegen_2_0`, `nano_banana_2`, `soul_v2`, `text2image_soul_v2`, `soul_cinematic`, `soul_cast`, `soul_location`, `seedream_v5_lite`, `seedream_v4_5`, `seedance_2_0`, `kling3_0`.

**Tier 2 — port after Tier 1 works, only if someone uses them:**
`image_auto`, `nano_banana`, `flux_2`, `openai_hazel`, `kling_omni_image`, `grok_image`, `z_image`, `seedance1_5`, `cinematic_studio_2_5`, `cinematic_studio_3_0`, `kling2_6`, `minimax_hailuo`, `wan2_6`, `wan2_7`, `veo3`, `veo3_1`, `veo3_1_lite`, `grok_video`, `claudesfield_video`.

---

## 3. Strategy

**Port directly.** Since the CLI is being deprecated, we cannot wrap it —
reimplement in Python. To keep this tractable:

- One HTTP client module, not one per model. The only per-model code is
  defaults + validation + dimension lookup + request shape. Everything else
  (auth, do, retry, poll, error mapping) is shared.
- One tool schema with a `oneOf` on `model` — matches the CLI's own
  `generate --json` interface. The tool itself routes to a per-model
  param-builder.
- Strict input validation before the HTTP call (mirror each `runXxxFromInput`
  function). Same error messages as the Go so existing docs/skill examples
  still apply.
- **Media ID upload is out of scope** — callers must supply pre-existing
  media IDs. If `type`/`url` are omitted we resolve via `GET /input-images/{id}`,
  same as the Go. Surfaces an open question about who owns upload after
  CLI deprecation (see §7).

---

## 4. Tool decomposition

Minimal surface. Two tools:

| Tool | Purpose |
|---|---|
| `higgsfield_generate` | Submit → poll → return result. Blocks by default; `async=true` returns `{job_ids}` immediately. |
| `higgsfield_job_status` | Poll an existing `job_id` to completion and return its result. Used when `async=true` was set earlier, or to resume after a timeout. |

**Why not one per model:** 28 near-identical tools would bloat the tool list
and the LLM would have to pick between overlapping names. Union schema is
verbose but the model-selector is unambiguous and lets us delete the schema
union entries cleanly as models are retired.

**Why `higgsfield_job_status` even though it's not `generate`:** if a submit
times out or runs `async=true`, the agent needs a way to resume. That's a
tool, not a CLI wrapper — it's using the same HTTP client against a job we
already created.

---

## 5. File layout

All files are discoverable by `tools/registry.py:56` (top-level `tools/*.py`
modules with a top-level `registry.register(...)` call). Shared modules
without a register call are skipped by the AST scan, so they're safe to keep
alongside.

```
tools/
  higgsfield_generate.py       # tool: higgsfield_generate (registers)
  higgsfield_job_status.py     # tool: higgsfield_job_status (registers)
  higgsfield/                  # package of shared internals (NOT scanned)
    __init__.py
    client.py                  # HTTP client (httpx.Client or requests)
    auth.py                    # build headers from env
    errors.py                  # HiggsfieldError + APIError mapping
    polling.py                 # terminal statuses, poll loop
    media.py                   # resolve_media_inputs / resolve_image_inputs
    models/
      __init__.py
      registry.py              # {model_name: ModelBuilder}
      _base.py                 # ModelBuilder ABC — validate + build_params
      imagegen_2_0.py
      nano_banana_2.py
      soul_v2.py               # also handles text2image_soul_v2
      soul_cinematic.py
      soul_cast.py
      soul_location.py
      seedream_v5_lite.py
      seedream_v4_5.py
      seedance_2_0.py
      kling3_0.py
      # Tier 2 models added later in the same shape
```

A "ModelBuilder" is a small class that owns:
- `NAME`, aliases (`text2image_soul_v2` for `soul_v2`)
- Default values for each optional field
- Enum/range validators
- `ASPECT_DIMENSIONS: dict[str, tuple[int, int]]` when applicable
- `build_params(input: dict) -> dict` — returns the exact JSON body the API expects

---

## 6. Implementation phases

Each phase ships independently. A ModelBuilder under test is ~50–100 LOC;
Tier 1 is 11 of them.

### Phase 0 — HTTP skeleton (½ day)
- [ ] `tools/higgsfield/auth.py` — `build_headers()` reading `HF_DEV_USER_ID`, `HF_FOLDER_ID`, `HF_JWT_TOKEN`.
- [ ] `tools/higgsfield/client.py` — `HiggsfieldClient` with `create_job(job_set_type, params)`, `get_job_status(id)`, `get_job(id)`, `get_input_image(id)`. Use `httpx.Client` (sync) — `requests` is fine too but httpx is already in the Hermes dep tree.
- [ ] `tools/higgsfield/errors.py` — `HiggsfieldAPIError(status, body)`, `HiggsfieldConfigError(missing_env)`.
- [ ] `tools/higgsfield/polling.py` — `TERMINAL_STATUSES = {"completed", "canceled", "failed", "nsfw", "ip_detected"}`; `wait_for_job(client, job_id, interval=5, timeout=900)`.
- [ ] `tools/higgsfield/media.py` — `resolve_media_inputs(client, model, inputs)`, `resolve_image_inputs(client, inputs)`.
- [ ] Tests: mocked `httpx.Client`; verify header set, body shape, error mapping.

### Phase 1 — ModelBuilder skeleton + `imagegen_2_0` (½ day)
- [ ] `tools/higgsfield/models/_base.py` — `ModelBuilder` ABC. `validate(input) -> None`, `build_params(input, folder_id) -> dict`.
- [ ] `tools/higgsfield/models/registry.py` — registration decorator, `get_builder(model: str) -> ModelBuilder`.
- [ ] `tools/higgsfield/models/imagegen_2_0.py` — first real builder; port from `generation/imagegen2.go:142` (`runImagegen2FromInput`). Fixture: `aspect_ratio` → `(width, height)` from `generation/imagegen2.go:21`.
- [ ] Tests: golden-file test — input dict → exact expected params dict, for each enum combination.

### Phase 2 — `higgsfield_generate` tool (½ day)
- [ ] `tools/higgsfield_generate.py` with OpenAI-style schema: top-level properties shared by all models (`model`, `prompt`, `aspect_ratio`, `batch_size`, `folder_id`, `tool_use_id`, `medias`, `async`, `timeout_seconds`) + a `oneOf` on `model` for per-model requireds/enums. (Pragmatic: keep the schema loose — server validates; focus schema on telling the LLM which fields matter per model.)
- [ ] Handler: `build_headers()` → `get_builder(input["model"]).build_params(input)` → `client.create_job(...)` → if `async=true` return `{job_ids, job_set_id, job_set_type}`; else loop `wait_for_job` for each `job_id` and `client.get_job(...)` for results.
- [ ] `check_fn`: env vars present (`FNF_BASE_URL`, `HF_FOLDER_ID`, plus dev-or-prod auth).
- [ ] `requires_env`: `["FNF_BASE_URL", "HF_FOLDER_ID"]` + auth keys.
- [ ] Register under toolset `higgsfield`.

### Phase 3 — `higgsfield_job_status` tool (¼ day)
- [ ] `tools/higgsfield_job_status.py` — takes `{job_id, poll?=true, interval?=5, timeout_seconds?=900}`.
- [ ] Reuses `client.get_job_status` + `client.get_job`.
- [ ] Same toolset.

### Phase 4 — port Tier 1 models (2 days)
- [ ] `nano_banana_2` — from `generation/nano_banana.go`.
- [ ] `soul_v2` + `text2image_soul_v2` alias — from `generation/soul_v2.go`.
- [ ] `soul_cinematic` — from `generation/soul_cinematic.go`.
- [ ] `soul_cast` — from `generation/soul_cast.go` (has nested `character_params`).
- [ ] `soul_location` — from `generation/soul_location.go`.
- [ ] `seedream_v5_lite` — from `generation/seedream_v5_lite.go`.
- [ ] `seedream_v4_5` — from `generation/seedream_v4_5.go`.
- [ ] `seedance_2_0` — from `generation/video.go`.
- [ ] `kling3_0` — from `generation/kling3.go` (multi-shot, `kling_element_ids`).
- [ ] For each: golden-file test. Reuse fixtures from `generation/models_test.go` (Go test fixtures in JSON form — port them directly).

### Phase 5 — toolset + doctor (½ day)
- [ ] `toolsets.py`: add `higgsfield` toolset with both tools. Add `higgsfield` to `_HERMES_CORE_TOOLS` if desired (decision: **no** for v1 — opt-in via `hermes tools` until it's proven).
- [ ] `hermes_cli/doctor.py`: env-var presence is auto-surfaced by `requires_env`; add a probe that calls `GET /internal/claudesfield/balance` to confirm auth works end-to-end. (Balance endpoint is cheap and doesn't mutate anything.)

### Phase 6 — skill update (½ day)
- [ ] Audit `skills/` + `optional-skills/` for `higgsfieldcli` invocations. Replace `higgsfieldcli generate --json {...}` examples with `higgsfield_generate({...})` in SKILL.md files.
- [ ] Verify sub-agents (`marketing-agent`, `recreate-agent`, `image-agent`, `soul-id-agent`) that shell out to `higgsfieldcli` — either point them at the new tool or leave them as-is if they're out of this migration's scope (they're separate agents, but if they break after deprecation they need to migrate too).

### Phase 7 — port Tier 2 (optional, as needed)
Only port models when someone actually calls them. Follow the Tier 1 pattern.

---

## 7. Open questions

1. **Auth.** The Go client sets `hf-dev-user-id`, `hf-dev-folder-id`, `X-Claudesfield-Token` (`internal/api/client.go:60`). The README also mentions `HF_INTERNAL_API_KEY`, but it doesn't appear in the client. Confirm whether prod actually uses something in addition to JWT. Don't port phantom headers.
2. **Who owns media upload post-CLI?** `generate` needs media IDs. Without upload there's no way to do image-to-image from a local file. Options: (a) ship a minimal `higgsfield_upload_media` tool alongside (small, uses the same client — add to scope); (b) require callers to upload via a separate service / UI; (c) expand scope later. Recommend **(a)** — upload is ~50 LOC and unblocks the whole image-to-image path.
3. **Tier 1 model list.** Confirmed against which skills / agents actually call them? Anything on the Tier 2 list that's actually Tier 1 in practice?
4. **Parallel requests.** Go supports `generate --json [ ... ]` with a goroutine per item. Python equivalent: loop with `concurrent.futures.ThreadPoolExecutor`, or expose parallelism via the agent calling the tool multiple times. Recommend **the latter** — Hermes's `delegate_task` / code-execution already handles parallel tool calls; batch-within-tool adds schema complexity for no win.
5. **Timeouts.** Go uses `FNF_TIMEOUT=30s` for the HTTP client but no wall-clock budget on polling. For the tool, use `httpx` timeout = `FNF_TIMEOUT` (default 30s) on individual requests, plus `timeout_seconds` (default 900) on the total poll. Match, or loosen?
6. **Retry.** Go has no retry. Should the port add one? Recommend **no** for v1 — let the agent retry at the tool-call level if a job fails transiently. Retrying `create-job` on a network blip risks double-billing.
7. **Testing against real FNF.** Need a dev user ID + folder ID that's safe to generate against. Behind an env flag (`HF_LIVE_TEST=1`) so CI doesn't burn credits.

---

## 8. Non-goals

- Exposing `upload-file`, `balance`, `connector`, `inspiration`, `element`, `soul-id`, `cron`, `skill publish`, `job-ip-check` as tools. (Upload may get pulled in — see Q2.)
- Reimplementing the `higgsfieldcli` flag-based per-model commands (`image`, `soul-v2`, etc.) — these were only for humans; agents always went through `generate --json`.
- Keeping the Go binary around as a fallback.
- Windows support — FNF is internal; assume Unix.
- MCP wrapping.

---

## 9. Success criteria

- `hermes -q "generate 'a cat in space' with imagegen_2_0"` produces a URL with no Go binary anywhere in the process tree.
- Tier 1 models all pass golden-file tests mirroring the Go test fixtures.
- Live integration test (behind `HF_LIVE_TEST=1`) runs one Tier 1 generation end-to-end and returns a usable URL.
- `hermes doctor` reports Higgsfield env vars + live auth probe status.
- Existing skills that used to call `higgsfieldcli generate` now reference `higgsfield_generate` and still work.
- Go binary can be removed from `~/.hermes/bin/` and nothing breaks.
