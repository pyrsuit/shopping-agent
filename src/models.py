from pydantic import BaseModel


class ShoppingItem(BaseModel):
    name: str
    quantity: str = "as needed"
    category: str = "other"


class ShoppingList(BaseModel):
    meals: list[str]
    items: list[ShoppingItem]
    notes: str = ""
