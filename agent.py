from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from models import ShoppingList

RECIPES: dict[str, list[str]] = {
    "pasta carbonara": ["spaghetti 400g", "guanciale 150g", "eggs 4", "parmesan 80g", "black pepper"],
    "greek salad": ["cucumber 1", "tomatoes 3", "red onion 1", "feta 200g", "olives 100g", "olive oil", "oregano"],
    "chicken stir-fry": ["chicken breast 500g", "broccoli 1 head", "bell pepper 2", "soy sauce", "garlic 3 cloves", "sesame oil", "ginger 1 piece"],
    "tomato soup": ["tomatoes 6", "onion 1", "garlic 3 cloves", "olive oil", "vegetable stock 500ml", "basil"],
    "caesar salad": ["romaine lettuce 1", "chicken breast 300g", "parmesan 50g", "croutons 100g", "caesar dressing 100ml"],
    "omelette": ["eggs 3", "butter 20g", "salt", "black pepper", "cheddar 50g"],
}

CATEGORIES: dict[str, str] = {
    "spaghetti": "pasta & grains",
    "guanciale": "meat & fish",
    "chicken breast": "meat & fish",
    "eggs": "dairy & eggs",
    "parmesan": "dairy & eggs",
    "feta": "dairy & eggs",
    "butter": "dairy & eggs",
    "cheddar": "dairy & eggs",
    "cucumber": "produce",
    "tomatoes": "produce",
    "red onion": "produce",
    "onion": "produce",
    "broccoli": "produce",
    "bell pepper": "produce",
    "romaine lettuce": "produce",
    "basil": "produce",
    "ginger": "produce",
    "olives": "deli & condiments",
    "olive oil": "oils & condiments",
    "soy sauce": "oils & condiments",
    "sesame oil": "oils & condiments",
    "caesar dressing": "oils & condiments",
    "croutons": "bakery & snacks",
    "vegetable stock": "canned & dry goods",
    "oregano": "spices",
    "black pepper": "spices",
    "salt": "spices",
    "garlic": "produce",
}

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
        "Return a structured shopping list."
    ),
)


@shopping_agent.tool
def get_inventory(ctx: RunContext[dict]) -> dict[str, str]:
    """Returns the current home inventory as a dict of item name to quantity."""
    return ctx.deps


@shopping_agent.tool
def get_recipe_ingredients(ctx: RunContext[dict], meal: str) -> list[str]:
    """Returns the list of ingredients needed for a given meal name.
    The meal name should be lowercase (e.g. 'pasta carbonara').
    Returns an empty list if the recipe is not found."""
    return RECIPES.get(meal.lower(), [])


@shopping_agent.tool
def categorize_item(ctx: RunContext[dict], item: str) -> str:
    """Returns the grocery category for a given item name (e.g. 'produce', 'dairy & eggs').
    Returns 'other' if the category is unknown."""
    item_lower = item.lower()
    for key, category in CATEGORIES.items():
        if key in item_lower or item_lower in key:
            return category
    return "other"
