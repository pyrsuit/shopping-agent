# Smart Shopping List Agent

A home project using PydanticAI to plan weekly meals and generate structured shopping lists. You describe meals in plain English; the agent checks your inventory and outputs a typed, categorized shopping list.

## Project Structure

```
shopping_agent/
├── CLAUDE.md
├── pyproject.toml # uv project config and dependencies
├── uv.lock # lockfile (commit this)
├── main.py # Entry point and CLI
├── agent.py # PydanticAI agent definition and tools
├── models.py # Pydantic output models
├── inventory.py # Inventory read/write logic
├── inventory.json # Local inventory (source of truth)
├── tests/
│   ├── __init__.py
│   ├── test_inventory.py
│   └── test_agent.py
```

## Setup

**Dependency manager:** [uv](https://docs.astral.sh/uv/)

**Test runner:** [pytest](https://docs.pytest.org/)

### Initialize the project

```bash
uv init
uv add pydantic-ai anthropic
uv add --dev pytest pytest-asyncio
```

This generates `pyproject.toml` and `uv.lock`.

### Environment

```bash
export ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>
```

### Run the agent
 
```bash
uv run python main.py "I want to make pasta carbonara, Greek salad, and chicken stir-fry this week"
```

### Run tests
 
```bash
uv run pytest
uv run pytest -v # verbose
uv run pytest tests/test_inventory.py # single file
```
 
## Architecture

```
User input (natural language meal descriptions)
        ↓
  PydanticAI Agent  (claude-sonnet-4-6)
        ↓
  Tools (called automatically by the agent)
  ├── get_inventory()              → reads inventory.json
  ├── get_recipe_ingredients(meal) → returns ingredient list per meal
  └── categorize_item(item)        → assigns grocery aisle/category
        ↓
  ShoppingList (structured Pydantic output)
```
  
## Key Decisions
 
- **`agent.run_sync()`** in `main.py` — no concurrency needed in the CLI, keep it simple
- **`inventory.json`** is the single source of truth for what's at home; back it up before bulk edits
- **Tool docstrings** are sent to the LLM as tool descriptions — keep them clear and precise
- **`deps_type=dict`** injects the inventory into the agent without globals
- **Model:** `anthropic:claude-sonnet-4-6` — swap to any other supported model with no other code changes

## Development Milestones
 
1. **MVP** — hardcoded recipe dict + `inventory.json` + structured output ✅ start here
2. **Inventory CLI** — `--add "milk 1L"` / `--remove "milk"` flags in `main.py`
3. **Recipe API** — replace hardcoded dict with API calls
4. **Fuzzy matching** — "garlic cloves" should match "garlic" in inventory
5. **Web UI** — FastAPI backend + simple HTML frontend
6. **Stretch** — budget estimation, weekly meal planner mode, store-specific sorting

## Testing
 
**Runner:** pytest with `pytest-asyncio` (`asyncio_mode = "auto"` — no decorator needed on async tests).
 
- `tests/test_inventory.py` — tests for `inventory.py` CRUD logic; use `monkeypatch` to redirect `INVENTORY_FILE` to `tmp_path`
- `tests/test_agent.py` — tests for agent behavior; use PydanticAI's `TestModel` to avoid real API calls
