import sys
from dotenv import load_dotenv

load_dotenv()

from agent import shopping_agent
from inventory import load_inventory, add_item, remove_item


def print_shopping_list(result) -> None:
    shopping_list = result.output
    print(f"\nMeals planned: {', '.join(shopping_list.meals)}")
    print("\nShopping list:")

    by_category: dict[str, list] = {}
    for item in shopping_list.items:
        by_category.setdefault(item.category, []).append(item)

    for category, items in sorted(by_category.items()):
        print(f"\n  {category.upper()}")
        for item in items:
            print(f"    - {item.name}: {item.quantity}")

    if shopping_list.notes:
        print(f"\nNotes: {shopping_list.notes}")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  uv run python main.py \"<meal description>\"")
        print("  uv run python main.py --add \"<item> <quantity>\"")
        print("  uv run python main.py --remove \"<item>\"")
        print("  uv run python main.py --inventory")
        sys.exit(1)

    if args[0] == "--add" and len(args) >= 2:
        parts = args[1].rsplit(" ", 1)
        if len(parts) == 2:
            add_item(parts[0], parts[1])
            print(f"Added '{parts[0]}' ({parts[1]}) to inventory.")
        else:
            print("Usage: --add \"<item name> <quantity>\"")
        return

    if args[0] == "--remove" and len(args) >= 2:
        removed = remove_item(args[1])
        if removed:
            print(f"Removed '{args[1]}' from inventory.")
        else:
            print(f"'{args[1]}' not found in inventory.")
        return

    if args[0] == "--inventory":
        inventory = load_inventory()
        if not inventory:
            print("Inventory is empty.")
        else:
            print("Current inventory:")
            for item, qty in sorted(inventory.items()):
                print(f"  {item}: {qty}")
        return

    user_input = " ".join(args)
    inventory = load_inventory()
    print(f"Planning meals for: {user_input}")
    result = shopping_agent.run_sync(user_input, deps=inventory)
    print_shopping_list(result)


if __name__ == "__main__":
    main()
