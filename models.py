from pydantic import BaseModel


class ShoppingItem(BaseModel):
    name: str
    quantity: str
    category: str


class ShoppingList(BaseModel):
    meals: list[str]
    items: list[ShoppingItem]
    notes: str = ""
