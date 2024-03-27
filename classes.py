import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image
from sqlite3 import connect
import tkinter as tk
from collections import namedtuple


class MenuItem:
    def __init__(self,
                 number: int,
                 name: str,
                 price: float,
                 description: str,
                 ingredients: list,
                 flavours: list,
                 sauces: list):
        self.number = number
        self.name = name
        self.price = price
        self.description = description
        self.ingredients = ingredients
        self.flavours = flavours
        self.sauces = sauces


class Menu(list):
    def __init__(self,
                 db: str = 'menuitems.db',
                 table: str = 'menuitems'):
        super().__init__()
        self.initMenu(db=db, table=table)

    def initMenu(self, db: str, table: str):
        # Connecting to database and fetching all the data from it.
        conn = connect(db)
        cur = conn.cursor()

        # Fetch all the rows from the database
        dbItems = cur.execute('SELECT * FROM ' + table)
        dbItems = dbItems.fetchall()

        # Close the database
        cur.close()
        conn.close()

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
            self.append(item)


class Cart(list):
    def __init__(self):
        super().__init__()

    def edit(self, item: MenuItem, quantity: int, ingredients: list, flavours: list, sauces: list):
        self.append([item, quantity, ingredients, flavours, sauces])


class PaymentInfo(namedtuple):
    def __new__(cls, cardnum: int, expirydate: str, csv: int):
        return super().__init__(cardnum, expirydate, csv, field_names=('Card Number', 'Expiry Date', 'CSV'))

    def __init__(self, cardnum: int, expirydate: str, csv: int):
        self.__new__(cls=type(self), cardnum=cardnum, expirydate=expirydate, csv=csv)


class DeliveryInfo(namedtuple):
    def __new__(cls, ):


class Items(ScrolledFrame):
    def __init__(self,
                 *args,
                 master: ttk.Window,
                 menu: Menu,
                 height: int = 806,
                 width: int = 800,
                 cart: Cart,
                 **kwargs
                 ):
        super().__init__(*args, master=master, height=height, width=width, **kwargs)

        for item in menu:
            # Create a path for the item image.
            try:
                image = ImageTk.PhotoImage(Image.open(('images/' + str(item.number) + ".png")))
            except FileNotFoundError:  # If the image does not exist, open an N/A image instead.
                image = ImageTk.PhotoImage(Image.open('images/na.png'))

            addToCart = AddToCartPopup(master=master, width=700, height=700, item=item, cart=cart)

            # Create a button widget. Add the item name and the price, as well as the image from above. Compound
            # places the image above the text.
            itemButton = ttk.Button(master=self, text=(item.name + f'$%.2f' % item.price), image=image,
                                    command=addToCart, compound='top')

            # Weird workaround for images not displaying correctly.
            itemButton.image = image

            # Code to place the button from above into a grid of 3 x infinite.
            column = (item.number - 1) - (((item.number - 1) // 3) * 3)
            row = (item.number - 1) // 3

            # Display the button in the grid.
            itemButton.grid(row=row, column=column, padx=5, pady=5)


class AddToCartPopup(ttk.Frame):
    def __init__(self,
                 *args,
                 master: ttk.Window,
                 item: MenuItem,
                 cart: Cart,
                 **kwargs):
        super().__init__(*args, master=master, **kwargs)

        try:
            itemImage = ImageTk.PhotoImage(Image.open(fp=f'images/%s.png' % item.number))
        except FileNotFoundError:
            itemImage = ImageTk.PhotoImage(Image.open(fp='images/na.png'))

        imageLabel = ttk.Label(master=self, image=itemImage)
        imageLabel.grid(column=0, row=0, columnspan=2)
        imageLabel.image = itemImage

        nameLabel = ttk.Label(master=self, text=item.name, font='Helvetica 14')
        nameLabel.grid(column=0, row=1, padx=5, pady=10, sticky='e')

        priceLabel = ttk.Label(master=self, text=f'$%.2f' % item.price, font='Helvetica 14')
        priceLabel.grid(column=1, row=1, padx=5, pady=5, sticky='w')

        descriptionLabel = ttk.Label(master=self, text=item.description)
        descriptionLabel.grid(column=0, row=3, padx=5, pady=5, columnspan=2)

        ingredients = OptionBox(master=self, inputType='checkbox', options=item.ingredients)
        ingredients.configure(text='Ingredients')
        ingredients.grid(column=0, row=4, padx=20, pady=5, columnspan=2)

        sauces = OptionBox(master=self, inputType='radio', options=item.sauces)
        sauces.configure(text='Sauces')
        sauces.grid(column=0, row=5, padx=20, pady=5, columnspan=2)

        flavours = OptionBox(master=self, inputType='radio', options=item.flavours)
        flavours.configure(text='Flavours')
        flavours.grid(column=0, row=6, padx=20, pady=5, columnspan=2)

        quantity = QuantitySpinBox(master=self, height=20)
        quantity.grid(column=0, row=7, padx=20, pady=20, columnspan=2)

        # TODO make it so that if there isn't a flavour, sauce or ingredients array it doesnt freak the fuck out.
        addToCartButton = ttk.Button(master=self,
                                     text='Add To Cart',
                                     command=lambda: self.addToCart(self=self,
                                                                    item=item,
                                                                    cart=cart,
                                                                    quantity=quantity.get(),
                                                                    ingredients=ingredients.GetChosenOptions(),
                                                                    sauces=sauces.GetChosenOptions(),
                                                                    flavours=flavours.GetChosenOptions())
                                     )
        addToCartButton.grid(column=0, row=8, padx=10, pady=10)

        closeButton = ttk.Button(master=self, text='Close', command=self.closePopup)
        closeButton.grid(column=1, row=8, padx=10, pady=10)

    def __call__(self):
        self.grid(column=0, row=0)

    def closePopup(self):
        self.grid_forget()

    @staticmethod
    def addToCart(self, cart: Cart, item: MenuItem, quantity: int, ingredients: list, flavours: list, sauces: list):
        cart.edit(item=item, quantity=quantity, ingredients=ingredients, flavours=flavours, sauces=sauces)
        self.closePopup()


class OptionBox(ttk.Labelframe):
    def __init__(self,
                 *args,
                 master: ttk.Frame,
                 inputType: str,
                 options: list,
                 **kwargs):
        super().__init__(*args, master=master, **kwargs)

        self.chosenoptions = list()

        checkboxvar = tk.StringVar()
        optionvars = list()

        try:
            options[0]
        except TypeError:
            self.chosenoptions.clear()
            self.chosenoptions.append('N/A')

            ttk.Label(self, text='N/A').grid(column=0, row=0)
        else:
            row = 0
            for option in options:
                if inputType == 'checkbox':
                    optionvar = tk.StringVar()
                    optionvars.append(optionvar)
                    button = ttk.Checkbutton(master=self,
                                             text=option,
                                             variable=optionvar,
                                             onvalue=option)
                elif inputType == 'radio':
                    button = ttk.Radiobutton(master=self,
                                             text=option, value=option,
                                             variable=checkboxvar,
                                             command=lambda: self.chosenoptions.append(checkboxvar.get()))

                button.grid(column=0, row=row)
                row = row + 1

            try:
                if inputType == 'checkbox':
                    for var in optionvars:
                        self.chosenoptions.append(var.get())
                    for i in range(len(self.chosenoptions)):
                        if self.chosenoptions[i] == '' or 'N/A':
                            self.chosenoptions.pop(i)
                elif inputType == 'radio':
                    self.chosenoptions[0] = self.chosenoptions[-1]
                    for i in range(len(self.chosenoptions[1:-1])):
                        self.chosenoptions.pop(i + 1)
            except IndexError:
                self.chosenoptions.clear()
                self.chosenoptions.append('N/A')

    def GetChosenOptions(self):
        return self.chosenoptions


class CartButton(ttk.Frame):
    def __init__(self,
                 *args,
                 cart: Cart,
                 delivery: DeliveryInfo,
                 payment: PaymentInfo,
                 **kwargs):
        super().__init__(*args, **kwargs)

        # Cart icon
        image = ImageTk.PhotoImage(Image.open('images/cart_new.png').resize((200, 200)))

        self.cartButton = ttk.Button(master=self, image=image, command=lambda: self.goToCart(cart=cart, payment=payment, delivery=delivery))
        self.cartButton.image = image

        cartNumber = ttk.Label(master=self, text='0', background='#be1a1a', font='Helvetica 18',
                               foreground='black')

        cartNumber.grid(row=0, column=0, sticky='ne', padx=39, pady=22)

        self.cartButton.grid(column=0, row=0, sticky='ne')

    @staticmethod
    def goToCart(cart: Cart, payment: PaymentInfo, delivery: DeliveryInfo):
        cartPage = ViewCartPage(cart=cart, payment=payment, delivery=delivery)
        cartPage.grid(row=0, column=0, sticky='nsew')

    def updateButton(self, cart: Cart):
        number = len(cart)
        self.cartButton.configure(text=number)


class ViewCartPage(ttk.Frame):
    def __init__(self, *args, cart: Cart, payment: PaymentInfo, delivery: DeliveryInfo, **kwargs):
        super().__init__(*args, **kwargs)

        items = ScrolledFrame(master=self)
        row = 0
        for item in cart:
            itemFrame = ttk.Frame(master=items)

            try:
                image = ImageTk.PhotoImage(Image.open(f'images/%s.png' % item[0].number).resize((50, 50)))
            except FileNotFoundError:
                image = ImageTk.PhotoImage(Image.open('images/na.png').resize((50, 50)))

            itemImage = ttk.Label(master=itemFrame, image=image, text=f'%s $%.2f' % (item[0].name, item[0].price),
                                  compound='left')
            itemImage.grid(row=0, column=0, padx=5, pady=10)

            itemImage.image = image

            itemIngredients = ttk.Label(master=itemFrame, text=item[2])
            itemIngredients.grid(column=1, row=0, padx=5, pady=10)

            itemFlavours = ttk.Label(master=itemFrame, text=item[3])
            itemFlavours.grid(column=2, row=0, padx=5, pady=10)

            itemSauces = ttk.Label(master=itemFrame, text=item[4])
            itemSauces.grid(column=3, row=0, padx=5, pady=10)

            itemQuantity = QuantitySpinBox(master=itemFrame, initial=item[1],
                                           command=lambda: self.UpdateCart(cart, item[0], itemQuantity.get()),
                                           width=40)
            itemQuantity.grid(column=4, row=0, padx=5, pady=10)

            itemFrame.grid(column=0, row=row, columnspan=2, padx=5, pady=10)
            row += 1

        items.grid(column=0, row=0, padx=5, pady=5)

        paymentFrame = ttk.Frame(master=self, borderwidth=5)

        numberLabel = ttk.Label(master=paymentFrame, text=payment[0])
        numberLabel.grid(column=0, row=0, padx=5, pady=5)

        csvLabel = ttk.Label(master=paymentFrame, text=payment[2])
        csvLabel.grid(column=0, row=1, padx=5, pady=5)

        expiryLabel = ttk.Label(master=paymentFrame, text=payment[1])
        expiryLabel.grid(column=0, row=2, padx=5, pady=5)

        paymentFrame.grid(column=0, row=1, padx=5, pady=5)

        deliveryFrame = ttk.Frame(master=self, borderwidth=5)

        deliveryFrame.grid(column=0, row=1, padx=5, pady=5)

        closeButton = ttk.Button(master=self, text='Close', command=self.closePopup)
        closeButton.grid(column=1, row=2, padx=5)

    def closePopup(self):
        self.grid_forget()

    @staticmethod
    def UpdateCart(cart: Cart, item: MenuItem, quantity: int):
        for i in range(len(cart)):
            if cart[i][0] == item:
                cart[i][1] = quantity


class QuantitySpinBox(ttk.Frame):
    def __init__(self,
                 *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: int = 1,
                 initial: int = 1,
                 command=None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subButton = ttk.Button(self, text='-', width=15, command=self.subButtonCallback)
        self.subButton.grid(row=0, column=2, padx=(3, 0), pady=3)

        self.addButton = ttk.Button(self, text='+', width=15, command=self.addButtonCallback)
        self.addButton.grid(row=0, column=0, padx=(0, 3), pady=3)

        self.entry = ttk.Entry(self, width=25)
        self.entry.grid(row=0, column=1, padx=3, pady=3, sticky='ew')

        self.entry.insert(0, str(initial))

    def addButtonCallback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            self.entry.delete(0, 'end')
            self.entry.insert(0, str(value))
        except ValueError:
            return

    def subButtonCallback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            self.entry.delete(0, 'end')
            self.entry.insert(0, str(value))
        except ValueError:
            return

    def get(self) -> int or None:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, 'end')
        self.entry.insert(0, str(int(value)))
