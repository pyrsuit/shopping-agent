import json
from pathlib import Path

INVENTORY_FILE = Path(__file__).parent.parent / "data" / "inventory.json"


def load_inventory() -> dict[str, str]:
    if not INVENTORY_FILE.exists():
        return {}
    with INVENTORY_FILE.open() as f:
        return json.load(f)


def save_inventory(inventory: dict[str, str]) -> None:
    with INVENTORY_FILE.open("w") as f:
        json.dump(inventory, f, indent=2)


def add_item(name: str, quantity: str) -> None:
    inventory = load_inventory()
    inventory[name.lower()] = quantity
    save_inventory(inventory)


def remove_item(name: str) -> bool:
    inventory = load_inventory()
    key = name.lower()
    if key not in inventory:
        return False
    del inventory[key]
    save_inventory(inventory)
    return True
