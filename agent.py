from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from models import ShoppingList

model = OllamaModel(
    "llama3.2:3b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

shopping_agent = Agent(
    model,
    deps_type=dict,
    output_type=ShoppingList,
    retries=3,
    system_prompt=(
        "You are a helpful shopping assistant. Given meal descriptions, "
        "use the provided tools to check the inventory, get recipe ingredients, "
        "and categorize items. Only include items the user doesn't already have. "
        "Always respond in the same language the user writes in. "
        "Always respond with valid JSON matching this structure:\n"
        '{"meals": ["meal name"], "items": [{"name": "item", "quantity": "amount", "category": "category"}], "notes": ""}'
    ),
)


@shopping_agent.tool
def get_inventory(ctx: RunContext[dict]) -> dict[str, str]:
    """Returns the current home inventory as a dict of item name to quantity."""
    return ctx.deps
