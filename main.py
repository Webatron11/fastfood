from classes import Items, CartButton, Menu, Cart, PaymentInfo, DeliveryInfo
import ttkbootstrap as ttk

# Set up the window with its size, minimum size and max size.
# 225x225 images, then a random constant because it works.

windowSize = [(225 * 3) + 131, (225 * 3) + 350]
root = ttk.Window(size=windowSize,
                  minsize=windowSize,
                  maxsize=windowSize,
                  title='Fast Food Ordering Thing',
                  themename='litera')

menu = Menu(db='menuitems.db', table='menu')
cart = Cart()
payment = PaymentInfo(1111222233334444, '01/24', 123)
delivery = DeliveryInfo(number="10a", street="Ashford Pde", suburb="Merwether Heights", city="Newcastle", state="NSW",
                        postcode=2291, time='12:00', method=True)

items = Items(master=root, menu=menu, height=(225 * 3) + 131, width=(225 * 3) + 125, cart=cart)
items.grid(column=0, row=0)

cartFrame = CartButton(master=root, cart=cart, delivery=delivery, payment=payment)
cartFrame.grid(column=0, row=1, sticky='se', padx=20, pady=5)

root.mainloop()

for i in cart:
    print(i[0].name, i[1], i[2], i[3], i[4])

# TODO Add cart page
# TODO Add credit card input page
# TODO Add delivery info page
