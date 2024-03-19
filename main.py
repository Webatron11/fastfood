from sqlite3 import connect
import tkinter as tk
from classes import *
from PIL import ImageTk, Image

conn = connect('menuitems.db')
cur = conn.cursor()

dbItems = cur.execute('SELECT * FROM menuitems')
dbItems = dbItems.fetchall()

cur.close()
conn.close()

menu = Menu([])

for i in dbItems:
    item = MenuItem(i[0], i[1], i[2], i[3], i[4], i[5]. i[6], i[7])
    menu.add(item)

# Set up the window
window = tk.Tk()
window.title("Food Ordering")
window.resizable(width=False, height=False)

# Create frame for menu items display
menu_items = tk.Frame(master=window)

for item in menu.menu:
    tk.Frame(master=menu_items)
    img = ImageTk.PhotoImage(Image.open(item.image))
    tk.Label(image=img)

# # Create the Fahrenheit entry frame with an Entry
# # widget and label in it
# frm_entry = tk.Frame(master=window)
# ent_temperature = tk.Entry(master=frm_entry, width=10)
# lbl_temp = tk.Label(master=frm_entry, text="FFFF")
#
# # Layout the temperature Entry and Label in frm_entry
# # using the .grid() geometry manager
# ent_temperature.grid(row=0, column=0, sticky="e")
# lbl_temp.grid(row=0, column=1, sticky="w")
#
# # Create the conversion Button and result display Label
# btn_convert = tk.Button(
#     master=window,
#     text="\N{RIGHTWARDS BLACK ARROW}",
#     command=fahrenheit_to_celsius
# )
# lbl_result = tk.Label(master=window, text="POPP")
#
# # Set up the layout using the .grid() geometry manager
# frm_entry.grid(row=0, column=0, padx=10)
# btn_convert.grid(row=0, column=1, pady=10)
# lbl_result.grid(row=0, column=2, padx=10)
#
# # Run the application
# window.mainloop()
