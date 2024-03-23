from classes import *
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image
from sqlite3 import connect


def addItemToCart(root: ttk.Window(), item: MenuItem):
    addtocart = ttk.Frame(master=root, width=700, height=700)

    itemimage = ImageTk.PhotoImage(Image.open(fp=f'images/%s.png' % item.number))
    imagelabel = ttk.Label(master=addtocart, image=itemimage)
    imagelabel.grid(column=0, row=0)
    imagelabel.image = itemimage

    namelabel = ttk.Label(master=addtocart, text=item.name)
    namelabel.grid(column=0, row=1, padx=5, pady=5)

    pricelabel = ttk.Label(master=addtocart, text=item.price)
    pricelabel.grid(column=0, row=2, padx=5, pady=5)

    descriptionlabel = ttk.Label(master=addtocart, text=item.description)
    descriptionlabel.grid(column=0, row=3, padx=5, pady=5)

    quantity = ttk.Frame(master=addtocart)

    addbutton = ttk.Button(master=quantity)

    subtractbutton = ttk.Button(master=quantity)

    numberofitemsentry = ttk.Entry(master=quantity)


def initMenu(db: str, tableName: str):
    # Connecting to database and fetching all the data from it.
    conn = connect(db)
    cur = conn.cursor()

    # Fetch all the rows from the database
    dbItems = cur.execute('SELECT * FROM ' + tableName)
    dbItems = dbItems.fetchall()

    # Close the database
    cur.close()
    conn.close()

    # Initialise new Menu class with an empty list for the menu
    menu = Menu([])

    for i in dbItems:
        # Try to split the data from the database, if it doesn't work it assigns None instead.
        try:
            ingredients = list(i[4].split(", "))
        except AttributeError:
            ingredients = None

        try:
            flavours = list(i[5].split(", "))
        except AttributeError:
            flavours = None

        try:
            sauces = list(i[6].split(", "))
        except AttributeError:
            sauces = None

        # Initializes new item with data from the database
        item = MenuItem(i[0], i[1], i[2], i[3], ingredients, flavours, sauces)
        menu.add(item)

    return menu


def drawItems(root: ttk.Window, menu: Menu):
    # Creates a frame from TTKBootstrap that can be scrolled. The height and width comes from the same sizes as above.
    items = ScrolledFrame(root, height=(225 * 3) + 131, width=(225 * 3) + 125)

    # For each item from the database:
    for item in menu.menu:
        # Create a path for the item image.
        try:
            image = Image.open('/home/dakka/Git/fastfood/images/' + str(item.number) + ".png")
        except FileNotFoundError:  # If the image does not exist, open an N/A image instead.
            image = Image.open(fp='/home/dakka/Git/fastfood/images/na.png')

        image = ImageTk.PhotoImage(image)

        # Create a button widget. Add the item name and the price, as well as the image from above. Compound places the
        # image above the text.
        itemButton = ttk.Button(master=items, command=addItemToCart,
                                text=(item.name + " $" + str(item.price)),
                                compound='top'
                                )

        # Weird workaround for images not displaying correctly.
        itemButton.image = image

        # Code to place the button from above into a grid of 3 x infinite.
        column = (item.number - 1) - (((item.number - 1) // 3) * 3)
        row = (item.number - 1) // 3

        # Display the button in the grid.
        itemButton.grid(row=row, column=column, padx=5, pady=5)

    # Display the items grid.
    items.grid(column=0, row=0)


def drawCart(root: ttk.Window()):
    cartFrame = tk.Frame(root)

    # Cart icon
    image = ImageTk.PhotoImage(Image.open('images/cart_icon.png'))
    # Creating cart canvas with number in top right. Make it clickable
    cart = ttk.Label(master=cartFrame, image=image)
    cart.image = image

    cart = ttk.Canvas()
    cart.create_oval(0, 0, 20, 20, fill='red')
    cart.create_text(10, 10, text='1')

    cart.grid(column=0, row=0, sticky='ne')

    cartFrame.grid(column=0, row=0, sticky='se')
