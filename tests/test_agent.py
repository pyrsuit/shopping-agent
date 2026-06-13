import pytest
from pydantic_ai.models.test import TestModel
from pydantic_ai import capture_run_messages
from agent import shopping_agent
from models import ShoppingList, ShoppingItem


@pytest.fixture
def empty_inventory():
    return {}


@pytest.fixture
def stocked_inventory():
    return {"olive oil": "500ml", "garlic": "1 bulb", "soy sauce": "200ml"}


def test_agent_returns_shopping_list(empty_inventory):
    with shopping_agent.override(model=TestModel()):
        result = shopping_agent.run_sync("pasta carbonara", deps=empty_inventory)
    assert isinstance(result.output, ShoppingList)


def test_shopping_list_has_meals(empty_inventory):
    with shopping_agent.override(model=TestModel()):
        result = shopping_agent.run_sync("pasta carbonara and greek salad", deps=empty_inventory)
    assert isinstance(result.output.meals, list)


def test_shopping_list_items_are_typed(empty_inventory):
    with shopping_agent.override(model=TestModel()):
        result = shopping_agent.run_sync("omelette", deps=empty_inventory)
    for item in result.output.items:
        assert isinstance(item, ShoppingItem)
        assert item.name
        assert item.quantity
        assert item.category


def test_get_inventory_tool_called(stocked_inventory):
    with shopping_agent.override(model=TestModel()):
        with capture_run_messages() as messages:
            shopping_agent.run_sync("chicken stir-fry", deps=stocked_inventory)
    tool_names = [
        part.tool_name
        for msg in messages
        for part in getattr(msg, "parts", [])
        if hasattr(part, "tool_name")
    ]
    assert "get_inventory" in tool_names
