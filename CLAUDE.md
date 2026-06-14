# Smart Shopping List Agent

A home project using PydanticAI to plan weekly meals and generate structured shopping lists. You describe meals in plain English; the agent checks your inventory and outputs a typed, categorized shopping list.

## Project Structure

```
shopping-agent/
├── CLAUDE.md
├── pyproject.toml       # uv project config and dependencies
├── uv.lock              # lockfile (commit this)
├── README.md            # user-facing setup and usage
├── .env                 # local env vars (do not commit)
├── src/
│   ├── main.py          # entry point and CLI
│   ├── agent.py         # PydanticAI agent definition and tool
│   ├── models.py        # Pydantic output models
│   └── inventory.py     # inventory read/write logic
├── data/
│   └── inventory.json   # local inventory (source of truth)
└── tests/
    ├── __init__.py
    ├── test_inventory.py
    └── test_agent.py
```

## Commands

### Run the agent

```bash
uv run python src/main.py "pasta carbonara and greek salad this week"
```

### Inventory management

```bash
uv run python src/main.py --inventory          # view inventory
uv run python src/main.py --add "milk 1L"      # add item
uv run python src/main.py --remove "milk"      # remove item
```

### Run tests

```bash
uv run pytest
uv run pytest -v
uv run pytest tests/test_inventory.py  # single file
```

## Architecture

```
User input (natural language meal descriptions)
        ↓
  PydanticAI Agent (llama3.2:3b via Ollama)
        ↓
  get_inventory() tool → data/inventory.json
        ↓
  ShoppingList (structured Pydantic output)
        ↓
  CLI output grouped by category
```

## Key Decisions

- **Ollama + llama3.2:3b** — runs fully local via Docker; model set in `src/agent.py` via `OllamaModel` + `OllamaProvider(base_url="http://localhost:11434/v1")`
- **LLM handles recipes and categories** — no hardcoded lookup tables; the model knows ingredients and grocery categories on its own
- **`retries=3`** on the agent — small models sometimes produce malformed JSON; retries handle that gracefully
- **`deps_type=dict`** injects the inventory into the agent without globals; access it in tools via `ctx.deps`
- **`agent.run_sync()`** in `main.py` — no concurrency needed in the CLI, keep it simple
- **`data/inventory.json`** is the single source of truth for what's at home; back it up before bulk edits
- **python-dotenv** loads `.env` at startup in `main.py` before the agent is imported

## Roadmap

1. **MVP** — local LLM + `inventory.json` + structured output ✅
2. **Inventory CLI** — `--add` / `--remove` / `--inventory` flags ✅
3. **Fuzzy matching** — "garlic cloves" should match "garlic" in inventory
4. **Recipe API** — pull real recipes from an external source
5. **Stretch** — budget estimation, weekly meal planner mode, store-specific sorting

## Testing

**Runner:** pytest with `pytest-asyncio` (`asyncio_mode = "auto"` in `pyproject.toml` — no decorator needed on async tests). `pythonpath = ["src"]` set so tests can import from `src/` directly.

- `tests/test_inventory.py` — CRUD logic; uses `monkeypatch` to redirect `INVENTORY_FILE` to `tmp_path`
- `tests/test_agent.py` — agent behavior; uses PydanticAI's `TestModel` to avoid real model calls
