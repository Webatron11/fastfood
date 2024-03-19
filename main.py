from sqlite3 import connect
import tkinter as tk
import ttkbootstrap as ttk
from classes import *
from PIL import ImageTk, Image


def addItemToCart():
    print("test")


conn = connect('menuitems.db')
cur = conn.cursor()

dbItems = cur.execute('SELECT * FROM menuitems')
dbItems = dbItems.fetchall()

cur.close()
conn.close()

menu = Menu([])

for i in dbItems:
    ingredients = list(i[4].split(", "))
    flavours = list(i[5].split(", "))
    sauces = list(i[6].split(", "))
    item = MenuItem(i[0], i[1], i[2], i[3], ingredients, flavours, sauces)
    menu.add(item)

# Set up the window
root = tk.Tk()

items = tk.Frame(root)

for item in menu.menu:
    imagePath = 'images/' + str(item.number) + ".jpg"
    itemButton = ttk.Button(master=items, command=addItemToCart,
                            image=ImageTk.PhotoImage(Image.open(imagePath)),
                            text=(item.name + " $" + str(item.price)),
                            compound='left'
                            )

    column = item.number - ((item.number // 3) * 3)
    row = item.number // 3
    itemButton.grid(row=row, column=column, padx=5, pady=5)

items.grid()

root.mainloop()
