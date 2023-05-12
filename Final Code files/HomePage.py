from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps
from BusinessReport.BusinessReport import BusinessReport
from Order.Menu import Menu
from ViewOrders.ViewOrders import ViewOrders


class HomePage:
    def setup(self, root):
        # create a new frame for the home page
        home_frame = tk.Frame(root, width=800, height=500)
        home_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # set background picture for
        img = Image.open("menu_images/homepage.jpeg")
        resized_image = ImageOps.fit(img, (800, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(resized_image)
        background_label = tk.Label(home_frame, image=self.photo)  # set the photo as the background of the home frame
        background_label.pack(fill=tk.BOTH, expand=True)
        background_label.pack_propagate(False)  # don't adjust size to fit contents
        background_label.lift()

        # create a new instance of the ttk.Style class to manage the appearance of themed Tkinter widgets
        style = ttk.Style()
        style.theme_use("default")  # set the theme to be used by the style instance to the default theme on the current system
        
        # create instances of the Menu class, ViewOrders class and BusinessReport class
        place_order = Menu()
        view_orders = ViewOrders()
        business_report = BusinessReport()

        # set the buttons
        def btn(x, y, text, bcolor, fcolor, cmd):
            def on_enter(e):
                mybtn["background"]=bcolor
                mybtn["foreground"]=fcolor

            def on_leave(e):
                mybtn["background"]=fcolor
                mybtn["foreground"]=bcolor

            mybtn = Button(home_frame, width=24, height=2, text=text, font=("Arial", 15, "bold"),
                           fg=bcolor,
                           bg=fcolor,
                           highlightthickness=0,
                           relief="flat", 
                           borderwidth=0,
                           activeforeground=fcolor,
                           activebackground=bcolor,
                           command=cmd)
            mybtn.bind("<Enter>", on_enter)
            mybtn.bind("<Leave>", on_leave)

            mybtn.place(x=x, y=y)

        btn(280, 120, "Order", "black", "#c29060", place_order.menu_show)
        btn(280, 190, "View Order", "black", "#c29060", view_orders.view_order)
        btn(280, 260, "Business Report", "black", "#c29060", business_report.report)
        btn(280, 330, "Exit", "black", "#c29060", home_frame.quit)
        



