import tabulate


class Variable:
    def __init__(self, name, variabletype, displayformat, sizeinbyte, sizefordisplay, description, example, validation):
        self.name = name
        self.variabletype = variabletype
        self.displayformat = displayformat
        self.sizeinbyte = sizeinbyte
        self.sizefordisplay = sizefordisplay
        self.description = description
        self.example = example
        self.validation = validation


ItemName = Variable("ItemName",
                    "String",
                    "Burger",
                    "20",
                    "20",
                    "The name of the menu item",
                    "Burger, Hamburger, Large Drink, Ice Cream",
                    "Is Text. Is Title Case")

ItemPrice = Variable("ItemPrice",
                     "Float",
                     "$3132.31",
                     "8",
                     "8",
                     "The price of the item",
                     "Webb",
                     "Is Text. Is Title Case")

ItemDescription = Variable("ItemDescription",
                           "String",
                           "A delicious beef patty sandwiched by a beautiful white bun with tomato and lettuce.",
                           "50",
                           "50",
                           "A short description of the menu item",
                           "A delicious beef patty sandwiched by a beautiful white bun with tomato and lettuce.",
                           "Is text.")

ItemIngredients = Variable("ItemIngredients",
                           "Array",
                           "N/A",
                           "IDK",
                           "N/A",
                           "An array containing any ingredients contained in an item",
                           "['Tomato', 'Cheese', 'Hamburger Patty']",
                           "N/A")

ItemNumber = Variable("ItemNumber",
                      "Integer",
                      "N/A",
                      "1",
                      "N/A",
                      "A integer containing the item number.",
                      "0001",
                      "Is a number.")

ItemFlavours = Variable("ItemFlavours",
                        "Array",
                        "N/A",
                        "IDK",
                        "N/A",
                        "An array containing any flavours for an item. Will also contain any variations on an item, eg vegan/vego options",
                        "['Strawberry', 'Chocolate', 'Vanilla']",
                        "N/A")

ItemSauces = Variable("ItemSauces",
                      "Array",
                      "N/A",
                      "IDK",
                      "N/A",
                      "An array containing any sauces that can be added to an item",
                      "['Ketchup', 'Barbeque']",
                      "N/A")

FirstName = Variable("FirstName",
                     "String",
                     "Oscar",
                     "20",
                     "20",
                     "The first name of the person who controls the card used to purchase the items",
                     "Oscar",
                     "Is Text. Is Title Case")

LastName = Variable("LastName",
                    "String",
                    "Webb",
                    "20",
                    "20",
                    "The last name of the person who controls the card used to purchase the items",
                    "Webb",
                    "Is Text. Is Title Case")

CardNumber = Variable("CardNumber",
                      "Integer",
                      "1111 2222 3333 4444",
                      "16",
                      "16",
                      "An integer containing the card number for the user",
                      "1111 2222 3333 4444",
                      "Is int. Is 16 characters long")

CardSecurityCode = Variable("CardSecurityCode",
                            "Integer",
                            "111",
                            "1",
                            "1",
                            "An integer containing the card security code for the user",
                            "123",
                            "Is 3 characters, Is int")

CardExpiry = Variable("CardExpiry",
                      "Date",
                      "02/24",
                      "4",
                      "4",
                      "A date containing the month and year for the card's expiry",
                      "03/27",
                      "Month is <= 12 and >= this month, the year is >= current year and is 2 characters.")

Menu = Variable("Menu",
                "Array",
                "N/A",
                "IDK",
                "N/A",
                "An array containing all menu items",
                "[MenuItem 01, MenuItem 02, MenuItem 03]",
                "N/A")

AddressNumber = Variable("AddressNumber",
                         "String",
                         "10a",
                         "10",
                         "10",
                         "A string containing the number of the house or apartment for the address",
                         "10a",
                         "N/A")

AddressStreet = Variable("AddressStreet",
                         "String",
                         "Ashford Pde",
                         "50",
                         "50",
                         "The street name for the address",
                         "Ashford Pde",
                         "Is string")

AddressPostCode = Variable("AddressPostCode",
                           "Integer",
                           "2291",
                           "4",
                           "4",
                           "The post code for the address",
                           "2291",
                           "Is integer.")

AddressSuburb = Variable("AddressSuburb",
                         "String",
                         "Merewether Heights",
                         "30",
                         "30",
                         "The suburb name for the address",
                         "Merewether Heights",
                         "Is string")

AddressCity = Variable("AddressCity",
                       "String",
                       "Newcastle",
                       "30",
                       "30",
                       "The city for the address",
                       "Newcastle",
                       "Is String")

AddressState = Variable("AddressState",
                        "String",
                        "NSW",
                        "3",
                        "3",
                        "The abbreviated state name for the address",
                        "NSW",
                        "Is at least 2 characters. Is NSW, ACT, VIC, QLD, SA, WA, TAS, NT")

DeliveryOption = Variable("DeliveryOption",
                          "Boolean",
                          "N/A",
                          "1",
                          "N/A",
                          "A boolean describing whether the user wants their order delivered or picked up",
                          "TRUE",
                          "Is TRUE or FALSE")

DeliveryTime = Variable("DeliveryTime",
                        "Time",
                        "12:34",
                        "4",
                        "4",
                        "The time at which the user wishes their order to be ready",
                        "16:32",
                        "Is a valid 24 hr time")

Variables = [DeliveryTime, DeliveryOption, AddressCity, AddressState, AddressSuburb, AddressStreet, AddressNumber,
             AddressPostCode, ItemNumber, ItemSauces, ItemFlavours, ItemIngredients, ItemName, ItemPrice,
             ItemDescription, Menu, CardNumber, CardExpiry, CardSecurityCode, FirstName, LastName, LastName]

columnLabels = ['Name', 'Variable Type', 'Display Format', 'Size in Bytes', 'Size for Display', 'Description',
                'Example', 'Validation']
data = [
    [i.name, i.variabletype, i.displayformat, i.sizeinbyte, i.sizefordisplay, i.description, i.example, i.validation]
    for i in Variables]

print(tabulate.tabulate(data, headers=columnLabels, tablefmt="github"))
