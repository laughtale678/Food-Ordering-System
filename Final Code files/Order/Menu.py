import os
from PIL import ImageTk, Image, ImageOps
import tkinter as tk
from Order.MenuDetail import Menu_Detail


class Menu:
    def menu_show(self):
        order_frame = tk.Frame()
        order_frame.place(relx=0.5, rely=0.5, anchor='center')

        # set background picture
        img = Image.open("menu_images/homepage.jpeg")
        resized_image = ImageOps.fit(img, (800, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(resized_image)
        background_label = tk.Label(order_frame, image=self.photo) # set the photo as the background of the order frame
        background_label.pack(fill=tk.BOTH, expand=True)
        background_label.pack_propagate(False)  # don't adjust size to fit contents
        background_label.lift()

        # show menu details
        cafe_ui = Menu_Detail(order_frame)
        cafe_ui.setup_ui()


