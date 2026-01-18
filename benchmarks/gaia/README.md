# GAIA Benchmark Evaluation

This directory contains the implementation for running GAIA (General AI Assistants) benchmark evaluation using OpenHands agents.

## Overview

GAIA is a benchmark for evaluating AI assistants on real-world questions that require multi-step reasoning, web search, file processing, and tool use. Questions span 3 difficulty levels and often include supplementary files (images, documents, zip archives).

## Dataset

- **Source**: HuggingFace `gaia-benchmark/GAIA`
- **Levels**: `2023_level1`, `2023_level2`, `2023_level3`, `2023_all`
- **Splits**: `validation`, `test`

## Usage

### Prerequisites

Local GAIA evaluation uses Docker-based workspaces:

- Ensure Docker is installed and running:
  - `docker --version`
  - `docker run --rm hello-world`
- On non-linux system:
  - `docker buildx create --name openhands-builder --driver docker-container --use`
  - `docker buildx inspect --bootstrap` 
  - `export DOCKER_DEFAULT_PLATFORM=linux/amd64`

### Step 1: Run Inference

By default, GAIA uses a baseline MCP configuration that includes:
- `fetch` via `uvx mcp-server-fetch`
- `victor-websearch` via the public MCP endpoint at
  `https://victor-websearch.hf.space/gradio_api/mcp/sse`.

**Basic inference:**

```bash
uv run gaia-infer path/to/llm_config.json \
    --level 2023_level1 \
    --split validation
```

**Advanced options:**

```bash
uv run python -m benchmarks.gaia.run_infer \
    path/to/llm_config.json \
    --level 2023_level1 \
    --split validation \
    --max-iterations 100 \
    --n-limit 50 \
    --critic pass \
    --output-dir outputs/gaia \
    --num-workers 4
```

**🚨 Cedrus experiments (living in this fork/branch only):**

```bash
# GAIA inference with cedrus MCP tools enabled (baseline MCP + cedrus)
uv run gaia-cedrus-infer path/to/llm_config.json \
    --level 2023_level1 \
    --split validation \
    --max-iterations 100 \
    --output-dir outputs/gaia-cedrus \
    --num-workers 4
```

### Step 2: Get Score

After running inference, calculate the accuracy score:

```bash
uv run python -m benchmarks.gaia.get_score --file outputs/gaia/output.jsonl
```

## Configuration Options

### Required Arguments

- LLM config path: Path to JSON configuration file for the language model
- `--level`: GAIA level to evaluate (e.g., `2023_level1`, `2023_all`)
- `--split`: Dataset split (e.g., `validation`, `test`)

### Optional Arguments

- `--critic`: Critic to use for evaluation (default: `pass`)
- `--max-iterations`: Maximum iterations per instance (default: 30)
- `--output-dir`: Base directory for outputs (default: `outputs`)
- `--n-limit`: Limit number of instances to evaluate (default: 0 = all)
- `--num-workers`: Number of parallel workers (default: 1)
- `--max-attempts`: Maximum attempts for iterative mode (default: 1)
- `--note`: Optional note to add to output directory name


## Output Format

Results are written to JSONL files in the output directory. Each line contains:

```json
{
  "instance_id": "task_id_123",
  "test_result": {
    "score": true,
    "model_answer_raw": "The agent's full response...",
    "model_answer": "42",
    "ground_truth": "42"
  },
  "instruction": "The task instruction...",
  "history": [...],
  "instance": {...}
}
```


## References

- [GAIA Paper](https://arxiv.org/abs/2311.12983)
- [GAIA Dataset on HuggingFace](https://huggingface.co/datasets/gaia-benchmark/GAIA)
- [GAIA Leaderboard](https://huggingface.co/spaces/gaia-benchmark/leaderboard)
