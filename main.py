from functions import initMenu, drawCart, drawItems
import ttkbootstrap as ttk

# Set up the window with its size, minimum size and max size.
# 225x225 images, then a random constant because it works.

windowSize = [(225 * 3) + 131, (225 * 3) + 125]
root = ttk.Window(size=windowSize,
                  minsize=windowSize,
                  maxsize=windowSize,
                  title='Fast Food Ordering Thing',
                  themename='cyborg')

menu = initMenu('menuitems.db', 'menu')
drawItems(root, menu)
drawCart(root)

root.mainloop()
