# Shopping List Agent

Describe your meals in plain English and get a categorized shopping list — skipping anything you already have at home.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (for running Ollama)

## Setup

```bash
# 1. Start Ollama via Docker
docker compose up -d

# 2. Pull the model into the running container (one-time)
docker exec -it ollama ollama pull llama3.2:3b

# 3. Install dependencies
uv venv .venv
source .venv/bin/activate
uv sync
```

## Usage

```bash
# Plan meals → get a shopping list
uv run python src/main.py "pasta carbonara and greek salad this week"

# See what's in your inventory
uv run python src/main.py --inventory

# Add an item to inventory
uv run python src/main.py --add "milk 1L"

# Remove an item from inventory
uv run python src/main.py --remove "milk"
```
