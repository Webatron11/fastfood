"""
Menu Items
 - SQLite3 database containing item details
    - Item name
    - Price
    - Descriptions
    - Ingredients
        - Add and remove ingredients as wanted
    - Image (Path to Image)
    - Flavours
        - EG Drink flavours, ice cream flavours
    - Sauces
 - "MenuItem" class
 - Cart can be an array of "MenuItem" objects
"""


class MenuItem:
    def __init__(self, number: int, name: str, price: float, description: str, ingredients: list, flavours: list, sauces: list):
        self.number = number
        self.name = name
        self.price = price
        self.description = description
        self.ingredients = ingredients
        self.flavours = flavours
        self.sauces = sauces


class Menu:
    def __init__(self, menu: list):
        self.menu = menu

    def add(self, item: MenuItem):
        self.menu.append(item)
