# RL Training Smaller Models Using Hermes Traces

End-to-end guide: collect agent traces with a strong model, then use them to train a smaller model for your use cases.

---

## Pipeline Overview

```
1. COLLECT TRACES         2. COMPRESS              3. TRAIN
   (strong model)            (fit context)            (smaller model)

batch_runner.py      →   trajectory_compressor.py →  Option A: SFT (TRL)
  claude-sonnet            shrink to 29k tokens       Option B: GRPO (TRL)
  your prompts             keep head/tail turns        Option C: GRPO (Tinker-Atropos)
  ↓                        summarize middle             Option D: DPO (TRL)
  trajectory_samples.jsonl  ↓
                           compressed.jsonl
```

---

## Step 1: Prepare Your Prompts

Create a JSONL file with prompts representing your use cases:

```jsonl
{"prompt": "Analyze this CSV file and create a visualization of monthly trends"}
{"prompt": "Debug this Python error: KeyError in pandas DataFrame merge"}
{"prompt": "Set up a FastAPI endpoint with JWT authentication"}
{"prompt": "Write unit tests for the UserService class in tests/"}
```

**Tips:**
- Include diverse examples across your actual use cases
- 500-2000 prompts is a good starting point
- Add `"image"` field if prompts need specific Docker environments:
  ```jsonl
  {"prompt": "Install scikit-learn and train a classifier", "image": "python:3.11-slim"}
  ```

---

## Step 2: Collect Traces with a Strong Model

Run the batch runner against your prompts using a strong model (Claude Sonnet, GPT-4o, etc.):

```bash
python batch_runner.py \
    --dataset_file=data/my_prompts.jsonl \
    --batch_size=20 \
    --run_name=my_traces_v1 \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=8 \
    --max_turns=15
```

**Key flags:**

| Flag | Purpose |
|------|---------|
| `--num_workers` | Parallel workers (increase for speed, watch rate limits) |
| `--max_turns` | Max tool-call iterations per prompt |
| `--distribution` | Toolset distribution — `default` or custom (see `--list_distributions`) |
| `--reasoning_effort` | `none`, `low`, `medium`, `high`, `xhigh` |
| `--resume` | Resume from checkpoint if interrupted |
| `--max_tokens` | Max tokens per model response |

**Output:** `data/my_traces_v1/trajectories.jsonl` — ShareGPT-format JSONL with:
- Full conversation history (system, human, gpt, tool turns)
- Reasoning in `<think>` tags
- Tool calls in `<tool_call>` XML
- Tool stats and metadata

**Resume if interrupted:**
```bash
python batch_runner.py \
    --dataset_file=data/my_prompts.jsonl \
    --batch_size=20 \
    --run_name=my_traces_v1 \
    --resume
```

### Enabling traces in normal sessions

For ad-hoc collection from interactive sessions:

```yaml
# ~/.hermes/config.yaml
agent:
  save_trajectories: true
```

Or pass `--save-trajectories` to the CLI. Traces go to `trajectory_samples.jsonl` (successful) and `failed_trajectories.jsonl` (failed).

---

## Step 3: Compress Traces (Optional but Recommended)

Smaller models have shorter context windows. The compressor shrinks traces to fit while preserving the most important turns.

```bash
python trajectory_compressor.py \
    --input data/my_traces_v1/trajectories.jsonl \
    --config datagen-config-examples/trajectory_compression.yaml
```

**What it does:**
- Protects head turns (system prompt, first user message, first assistant response, first tool result)
- Protects tail turns (last N turns — the final answer)
- Summarizes the middle turns using a cheap LLM (Gemini Flash by default)
- Target: 29k tokens per trajectory (configurable)

**Config (`datagen-config-examples/trajectory_compression.yaml`):**

```yaml
tokenizer:
  name: "moonshotai/Kimi-K2-Thinking"  # match your target model's tokenizer

compression:
  target_max_tokens: 29000        # adjust for your target model's context
  summary_target_tokens: 750

protected_turns:
  first_system: true
  first_human: true
  first_gpt: true
  first_tool: true
  last_n_turns: 4

processing:
  num_workers: 4
  max_concurrent_requests: 50
```

**Output:** `data/my_traces_v1_compressed/` with compressed trajectories.

---

## Step 4: Train the Smaller Model

### Option A: Supervised Fine-Tuning (SFT)

Best for: teaching a model to follow the agent format and tool-calling patterns.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from peft import LoraConfig

# Load your target model
model_name = "Qwen/Qwen3-8B"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load compressed traces
dataset = load_dataset("json", data_files="data/my_traces_v1_compressed/trajectories.jsonl")

# Format for SFT — the conversations field is already in ShareGPT format
def format_conversation(example):
    messages = []
    for turn in example["conversations"]:
        role_map = {"system": "system", "human": "user", "gpt": "assistant", "tool": "tool"}
        messages.append({"role": role_map[turn["from"]], "content": turn["value"]})
    return {"messages": messages}

dataset = dataset.map(format_conversation)

# LoRA config for efficient training
lora_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

# Train
config = SFTConfig(
    output_dir="outputs/my-agent-sft",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
)

trainer = SFTTrainer(
    model=model,
    args=config,
    train_dataset=dataset["train"],
    processing_class=tokenizer,
    peft_config=lora_config,
)
trainer.train()
trainer.save_model("outputs/my-agent-sft/final")
```

### Option B: GRPO with TRL (Local)

Best for: training with reward signals on tasks where you can verify correctness.

Use the template at `skills/mlops/training/trl-fine-tuning/templates/basic_grpo_training.py`:

```python
from trl import GRPOTrainer, GRPOConfig
from peft import LoraConfig

# Define reward functions
def correctness_reward(completions, answer, **kwargs):
    """Check if model got the right answer."""
    rewards = []
    for completion in completions:
        # Your verification logic here
        correct = verify_answer(completion, answer)
        rewards.append(2.0 if correct else 0.0)
    return rewards

def format_reward(completions, **kwargs):
    """Reward proper tool-call XML format."""
    rewards = []
    for completion in completions:
        has_think = "<think>" in completion and "</think>" in completion
        has_tool = "<tool_call>" in completion and "</tool_call>" in completion
        rewards.append(0.5 if (has_think and has_tool) else 0.0)
    return rewards

config = GRPOConfig(
    output_dir="outputs/grpo-agent",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    max_prompt_length=2048,
    max_completion_length=4096,
    num_generations=4,        # completions per prompt (group size)
    learning_rate=4e-5,
    bf16=True,
    logging_steps=5,
)

lora_config = LoraConfig(r=32, lora_alpha=64, target_modules="all-linear")

trainer = GRPOTrainer(
    model="Qwen/Qwen3-8B",
    args=config,
    reward_funcs=[correctness_reward, format_reward],
    train_dataset=dataset,
    peft_config=lora_config,
)
trainer.train()
```

### Option C: GRPO with Tinker-Atropos (Distributed)

Best for: large-scale RL training with a managed training service.

**Prerequisites:**
```bash
# Initialize submodule
git submodule update --init tinker-atropos

# Install RL deps
uv pip install -e ".[rl]"

# Set API keys
echo "TINKER_API_KEY=your-key" >> ~/.hermes/.env
echo "WANDB_API_KEY=your-key" >> ~/.hermes/.env
```

**Create a custom environment** in `tinker-atropos/tinker_atropos/environments/my_task.py`:

```python
from tinker_atropos.environments.base import BaseEnv, BaseEnvConfig

class MyTaskConfig(BaseEnvConfig):
    dataset_name: str = "data/my_prompts.jsonl"
    group_size: int = 16
    batch_size: int = 128

class MyTaskEnv(BaseEnv):
    def __init__(self, config: MyTaskConfig):
        super().__init__(config)
    
    async def load_dataset(self):
        # Load your prompts/tasks
        ...
    
    async def get_next_item(self):
        # Return next prompt for the model
        ...
    
    async def score_answer(self, answer: str, item: dict) -> float:
        # Return reward [0.0, 1.0]
        # e.g., check if tool calls produced correct output
        ...
```

**Run training via the RL CLI:**
```bash
python rl_cli.py
# Then in the agent session:
# "List environments, select my_task, configure group_size=16, start training"
```

Or use the `rl_*` tools directly in a normal hermes session:
```
hermes chat --toolsets rl -q "Start RL training on the my_task environment"
```

**Training runs 3 processes:**
1. Atropos API (port 8000) — coordinates rollouts
2. Tinker trainer (port 8001) — LoRA training + inference
3. Environment — scoring + reward

**Monitor on WandB.** Logs: `~/.hermes/logs/rl_training/`

### Option D: DPO (Preference Alignment)

Best for: when you have pairs of good/bad trajectories.

```python
from trl import DPOTrainer, DPOConfig

# Need chosen/rejected pairs — e.g., from completed vs failed trajectories
# or from high-reward vs low-reward traces

config = DPOConfig(
    output_dir="outputs/dpo-agent",
    beta=0.1,                    # KL penalty weight
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=5e-5,
    bf16=True,
)

trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=preference_dataset,  # needs "chosen" and "rejected" columns
    processing_class=tokenizer,
    peft_config=lora_config,
)
trainer.train()
```

---

## Step 5: Evaluate

### Quick inference test (before full training)

The RL system has a built-in inference test that validates your environment works:

```
# In an RL session:
Test the selected environment with inference
```

This runs 3 steps x 16 completions across 3 model scales — no Tinker API needed.

### After training

1. **Merge LoRA weights** and deploy:
   ```python
   from peft import PeftModel
   
   base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B")
   model = PeftModel.from_pretrained(base, "outputs/my-agent-sft/final")
   merged = model.merge_and_unload()
   merged.save_pretrained("outputs/my-agent-merged")
   ```

2. **Serve via vLLM** and point hermes at it:
   ```bash
   vllm serve outputs/my-agent-merged --port 8000
   ```
   
   ```yaml
   # config.yaml
   llm:
     model: my-agent-merged
     base_url: http://localhost:8000/v1
     api_key: dummy
   ```

3. **Run eval prompts** through the batch runner with your fine-tuned model and compare tool_stats, completion rates, and quality vs the teacher model.

---

## Recommended Approach by Use Case

| Use case | Recommended path |
|----------|-----------------|
| **Teach tool-calling format** | SFT on compressed traces |
| **Improve task success rate** | GRPO with task-specific reward functions |
| **Large-scale RL with managed infra** | Tinker-Atropos GRPO |
| **Prefer good vs bad behavior** | DPO with completed vs failed trajectories |
| **Full pipeline** | SFT first → then GRPO or DPO for alignment |

## Key Files

| File | Purpose |
|------|---------|
| `batch_runner.py` | Parallel trace collection |
| `trajectory_compressor.py` | Compress traces to fit smaller context |
| `datagen-config-examples/trajectory_compression.yaml` | Compression config |
| `rl_cli.py` | RL-focused agent runner |
| `tools/rl_training_tool.py` | RL training tools (Tinker-Atropos) |
| `agent/trajectory.py` | Trajectory serialization logic |
| `skills/mlops/training/trl-fine-tuning/` | TRL training skill + GRPO template |
| `scripts/sample_and_compress.py` | Download + sample from HuggingFace datasets |
