import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import pandas as pd
import datetime


class Menu_Detail:
    def __init__(self, order_frame):
        self.order_frame = order_frame
        self.photos = []
        self.order_total = 0  # total price of all items in the table
        self.order_number = 1
        self.order_data = pd.DataFrame(columns=["Order Number", "Date", "Order Detail", "Order Total"])

        # ----------------------------------set background images----------------------------------------------
        # set top image
        top_image = Image.open("menu_images/top_image.png") 
        resized_image = top_image.resize((702, 100))
        top_img = ImageTk.PhotoImage(resized_image)
        top_img_label = tk.Label(self.order_frame, image=top_img)
        top_img_label.place(x=100, y=0, width=702, height=100)
        top_img_label.photo = top_img
        # set logo image
        logo_image = Image.open("menu_images/husky_coffee_logo.jpg") 
        resized_image = logo_image.resize((100, 100))
        logo_img = ImageTk.PhotoImage(resized_image)
        logo_img_label = tk.Label(self.order_frame, image=logo_img)
        logo_img_label.place(x=0, y=18, width=100, height=100)
        logo_img_label.photo = logo_img
        # set middle images
        middle_bg_image = Image.open("menu_images/middle_image.jpg")
        resized_image = middle_bg_image.resize((450, 402))
        middle_bg_img = ImageTk.PhotoImage(resized_image)
        middle_bg_img_label = tk.Label(self.order_frame, image=middle_bg_img)
        middle_bg_img_label.place(x=100, y=100, width=450, height=402)
        middle_bg_img_label.photo = middle_bg_img
        # set background of right area
        right_backgound = tk.Label(self.order_frame, foreground="white", background="#202020") 
        right_backgound.place(x =550, y=100, width=252, height=400)

        # -------------------------------create a table to display items---------------------------------------
        table_title = tk.Label(self.order_frame, text="Order Details", font=("Arial", 13, "bold"), fg="white", bg="black")
        table_title.place(x=550, y=100, width=252, height=20)
        columns = ("Name", "Quantity", "Total Price")
        self.table = ttk.Treeview(self.order_frame, columns=columns, show="headings")
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=84, anchor="center")
        self.table.place(x=550, y=120)
        # set up the bottom label to display total price
        self.order_total_label = tk.Label(self.order_frame, text="Order Total: $0")
        self.order_total_label.place(x=650, y=350)

    def close_order_frame(self):
        # destroy the order_frame window 
        self.order_frame.destroy()

    def setup_ui(self):
        # set left background label
        left_menu = tk.Label(self.order_frame, foreground="white", background="#202020")
        left_menu.place(x=0, y=100, width=100, height=402)

        # set menu title
        menu_detail_title = tk.Label(self.order_frame, text="Menu Details", font=("Arial", 13, "bold"), fg="white", bg="black")
        menu_detail_title.place(x=100, y=100, width=450, height=20)

        menu_title = tk.Label(self.order_frame, text="Menu", font=("Arial", 13, "bold"), fg="white", bg="black")
        menu_title.place(x=0, y=100,width=100,height=20)

        # show the coffee menu
        self.coffee_show()

        #--------------------------------------------set buttons---------------------------------------------------
        # set button style
        style = ttk.Style()  
        style.configure("RoundedButton.TButton", font=("Arial", 12, "bold"), borderwidth=0, padding=0, relief="flat", width=80, height=40)
        style.map("RoundedButton.TButton", background=[("active", "white")], foreground=[("active", "#c29060")])
       
        # set return button
        return_button = ttk.Button(self.order_frame, text="Return", style="RoundedButton.TButton", command=self.close_order_frame, state="normal")
        return_button.place(x=0, y=0, width=100, height=25)
        
        # set place order button
        order_button = ttk.Button(self.order_frame, text="Place Order", style="RoundedButton.TButton", command=self.place_order, state="normal")
        order_button.place(x=677, y=420, width=125, height=40)

        # set reset button
        reset_button = ttk.Button(self.order_frame, text="Reset", style="RoundedButton.TButton", command=self.reset, state="normal")
        reset_button.place(x=550, y=420, width=125, height=40)

        # set menu buttons
        def btn(x, y, text, bcolor, fcolor, cmd):
            def on_enter(e):
                mybtn["background"]=bcolor
                mybtn["foreground"]=fcolor

            def on_leave(e):
                mybtn["background"]=fcolor
                mybtn["foreground"]=bcolor

            mybtn = Button(self.order_frame, width=100, height=50, text=text, font=("Arial", 14),
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

            mybtn.place(x=x, y=y, width=100, height=50)

        btn(0, 140, "COFFEE", "black", "#c29060", self.coffee_show)
        btn(0, 210, "TEA", "black", "#c29060", self.tea_show)
        btn(0, 280, "FOODS", "black", "#c29060", self.foods_show)
        btn(0, 350, "OTHER"+"\n"+"BEVERAGES", "black", "#c29060", self.otherbeverage_show)

    def place_order(self):

        # ------------------------------Sort Data for View Orders-----------------------------------
        # get order number of current order (Increment previous order number by 1)
        try:
            prev_orders = pd.read_csv("order_data.csv")
        except FileNotFoundError:
            prev_orders = pd.DataFrame(columns=["Order Number", "Date", "Order Detail", "Order Total"])

        last_order_number = prev_orders.iloc[-1]["Order Number"] if not prev_orders.empty else 0
        self.order_number = last_order_number + 1

        # get date, order detail, order total of current order
        # add all data to the DataFrame
        order_detail = self.get_order_detail()

        # check if order detail is empty
        if not order_detail:
            messagebox.showerror(title="Error", message="Cannot place an empty order.", parent=self.order_frame)
            return
        
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.order_data = self.order_data.append({"Order Number": self.order_number,
                                                  "Date": date,
                                                  "Order Detail": order_detail,
                                                  "Order Total": round(self.order_total, 2)},
                                                 ignore_index=True)

        # save the DataFrame to a CSV file
        file_path = "order_data.csv"
        if os.path.exists(file_path):
            # append to the existing file
            self.order_data.to_csv(file_path, mode='a', header=False, index=False)
        else:
            # create a new file
            self.order_data.to_csv(file_path, index=False)

        # ----------------------Sort Data for Business Reports- item reports------------------------
        try:
            prev_orders = pd.read_csv("order_data.csv")
        except FileNotFoundError:
            prev_orders = pd.DataFrame(columns=["Order Number", "Date", "Order Detail", "Order Total"])
        # aggregate the quantity of each item sold
        item_counts = {}
        for order_detail_str in prev_orders["Order Detail"]:
            order_detail = eval(order_detail_str)
            for item, quantity_str in order_detail:
                quantity = int(quantity_str)  # Convert the quantity string to an integer
                if item in item_counts:
                    item_counts[item] += quantity
                else:
                    item_counts[item] = quantity
            # write the item counts to a new CSV file
            item_counts_df = pd.DataFrame(list(item_counts.items()), columns=["Item Name", "Quantity Sold"])
            item_counts_df.to_csv("item_counts.csv", index=False)

        # -------------------------Display the order confirmation message--------------------------
        messagebox.showinfo(title="Order Confirmation",
                            message=f'Your order has been placed successfully! \n '
                                    f'Order total would be ${self.order_total:.2f} ',
                            parent=self.order_frame)

        # -------------------------------------reset-----------------------------------------------
        self.reset()

    def reset(self):
        # destroy the popup window and return to the order_frame window to place another order
        self.order_total = 0
        self.order_total_label.config(text=f"Total Price: ${self.order_total:.2f}")
        self.table.delete(*self.table.get_children())
        self.order_data.drop(self.order_data.index, inplace=True)

    def get_order_detail(self):
        # get the table data
        table_data = self.table.get_children()
        order_detail = []
        # loop through the table data to retrieve the order details
        for item in table_data:
            name = self.table.item(item, "values")[0]
            quantity = self.table.item(item, "values")[1]
            order_detail.append((name, quantity))
        return order_detail

    def clear_window(self):
        for photo in self.photos:
            photo.destroy()
        self.photos = []

    # ---------------------------------------show menu----------------------------------------------
    def coffee_show(self):
        self.clear_window()
        # img1 + btn1
        image1 = Image.open("menu_images/coffee/AMERICANO.jpeg")
        resized_image = image1.resize((100, 100))
        img1 = ImageTk.PhotoImage(resized_image)
        img1_label = tk.Label(self.order_frame, image=img1)
        img1_label.place(x=110, y=120, width=100, height=100)
        img1_label.photo = img1
        self.photos.append(img1_label)

        coffee1_name = tk.Label(self.order_frame, text="AMERICANO", font=("Arial", 10))
        coffee1_name.place(x=110, y=220, width=100, height=10)
        self.photos.append(coffee1_name)

        coffeebtn1= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee1, state="normal")
        coffeebtn1.place(x=110, y=230, width=100, height=25)
        self.photos.append(coffeebtn1)

        # img2
        image2 = Image.open("menu_images/coffee/ THE BLACK TIE.jpeg")
        resized_image = image2.resize((100, 100))
        img2 = ImageTk.PhotoImage(resized_image)
        img2_label = tk.Label(self.order_frame, image=img2)
        img2_label.place(x=220, y=120, width=100, height=100)
        img2_label.photo = img2
        self.photos.append(img2_label)

        coffee2_name = tk.Label(self.order_frame, text="THE BLACK TIE", font=("Arial", 10))
        coffee2_name.place(x=220, y=220, width=100, height=10)
        self.photos.append(coffee2_name)

        coffeebtn2= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee2, state="normal")
        coffeebtn2.place(x=220, y=230, width=100, height=25)
        self.photos.append(coffeebtn2)

        # img3
        image3 = Image.open("menu_images/coffee/MACCHIATO.jpeg")
        resized_image = image3.resize((100, 100))
        img3 = ImageTk.PhotoImage(resized_image)
        img3_label = tk.Label(self.order_frame, image=img3)
        img3_label.place(x=330, y=120, width=100, height=100)
        img3_label.photo = img3
        self.photos.append(img3_label)

        coffee3_name = tk.Label(self.order_frame, text="MACCHIATO", font=("Arial", 10))
        coffee3_name.place(x=330, y=220, width=100, height=10)
        self.photos.append(coffee3_name)

        coffeebtn3= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee3, state="normal")
        coffeebtn3.place(x=330, y=230, width=100, height=25)
        self.photos.append(coffeebtn3)

        # img4
        image4 = Image.open("menu_images/coffee/CAPPUCCINO .jpeg")
        resized_image = image4.resize((100, 100))
        img4 = ImageTk.PhotoImage(resized_image)
        img4_label = tk.Label(self.order_frame, image=img4)
        img4_label.place(x=440, y=120, width=100, height=100)
        img4_label.photo = img4
        self.photos.append(img4_label)

        coffee4_name = tk.Label(self.order_frame, text="CAPPUCCINO", font=("Arial", 10))
        coffee4_name.place(x=440, y=220, width=100, height=10)
        self.photos.append(coffee4_name)

        coffeebtn4= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee4, state="normal")
        coffeebtn4.place(x=440, y=230, width=100, height=25)
        self.photos.append(coffeebtn4)

        # img5
        image5 = Image.open("menu_images/coffee/CAFFE LATTE.jpeg")
        resized_image = image5.resize((100, 100))
        img5 = ImageTk.PhotoImage(resized_image)
        img5_label = tk.Label(self.order_frame, image=img5)
        img5_label.place(x=110, y=270, width=100, height=100)
        img5_label.photo = img5
        self.photos.append(img5_label)

        coffee5_name = tk.Label(self.order_frame, text="CAFFE LATTE", font=("Arial", 10))
        coffee5_name.place(x=110, y=370, width=100, height=10)
        self.photos.append(coffee5_name)

        coffeebtn5= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee5, state="normal")
        coffeebtn5.place(x=110, y=380, width=100, height=25)
        self.photos.append(coffeebtn5)

        # img6
        image6 = Image.open("menu_images/coffee/CAFFE MOCHA.jpeg")
        resized_image = image6.resize((100, 100))
        img6 = ImageTk.PhotoImage(resized_image)
        img6_label = tk.Label(self.order_frame, image=img6)
        img6_label.place(x=220, y=270, width=100, height=100)
        img6_label.photo = img6
        self.photos.append(img6_label)

        coffee6_name = tk.Label(self.order_frame, text="CAFFE MOCHA", font=("Arial", 10))
        coffee6_name.place(x=220, y=370, width=100, height=10)
        self.photos.append(coffee6_name)

        coffeebtn6= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee6, state="normal")
        coffeebtn6.place(x=220, y=380, width=100, height=25)
        self.photos.append(coffeebtn6)

        # img7
        image7 = Image.open("menu_images/coffee/CARAMEL FRAPPÉ .jpeg")
        resized_image = image7.resize((100, 100))
        img7 = ImageTk.PhotoImage(resized_image)
        img7_label = tk.Label(self.order_frame, image=img7)
        img7_label.place(x=330, y=270, width=100, height=100)
        img7_label.photo = img7
        self.photos.append(img7_label)

        coffee7_name = tk.Label(self.order_frame, text="CARAMEL FRAPPÉ", font=("Arial", 10))
        coffee7_name.place(x=330, y=370, width=100, height=10)
        self.photos.append(coffee7_name)

        coffeebtn7= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee7, state="normal")
        coffeebtn7.place(x=330, y=380, width=100, height=25)
        self.photos.append(coffeebtn7)

        # img8
        image8 = Image.open("menu_images/coffee/ESPRESSO.png")
        resized_image = image8.resize((100, 100))
        img8 = ImageTk.PhotoImage(resized_image)
        img8_label = tk.Label(self.order_frame, image=img8)
        img8_label.place(x=440, y=270, width=100, height=100)
        img8_label.photo = img8
        self.photos.append(img8_label)

        coffee8_name = tk.Label(self.order_frame, text="ESPRESSO", font=("Arial", 10))
        coffee8_name.place(x=440, y=370, width=100, height=10)
        self.photos.append(coffee8_name)

        coffeebtn8= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_coffee8, state="normal")
        coffeebtn8.place(x=440, y=380, width=100, height=25)
        self.photos.append(coffeebtn8)

    def tea_show(self):
        self.clear_window()
        #img1
        image1 = Image.open("menu_images/tea/ICED MATCHA GREEN TEA LATTE.jpeg")
        resized_image = image1.resize((100, 100))
        img1 = ImageTk.PhotoImage(resized_image)
        img1_label = tk.Label(self.order_frame, image=img1)
        img1_label.place(x=110, y=120, width=100, height=100)
        img1_label .photo = img1
        self.photos.append(img1_label)

        tea1_name = tk.Label(self.order_frame, text="MATCHA", font=("Arial", 10))
        tea1_name.place(x=110, y=220, width=100, height=10)
        self.photos.append(tea1_name)

        teabtn1= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_tea1, state="normal")
        teabtn1.place(x=110, y=230, width=100, height=25)
        self.photos.append(teabtn1)

        # img2
        image2 = Image.open("menu_images/tea/BLACK TEA.jpeg")
        resized_image = image2.resize((100, 100))
        img2 = ImageTk.PhotoImage(resized_image)
        img2_label = tk.Label(self.order_frame, image=img2)
        img2_label.place(x=220, y=120, width=100, height=100)
        img2_label.photo = img2
        self.photos.append(img2_label)

        tea2_name = tk.Label(self.order_frame, text="BLACK TEA", font=("Arial", 10))
        tea2_name.place(x=220, y=220, width=100, height=10)
        self.photos.append(tea2_name)

        teabtn2= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_tea2, state="normal")
        teabtn2.place(x=220, y=230, width=100, height=25)
        self.photos.append(teabtn2)

        # img3
        image3 = Image.open("menu_images/tea/TROPICAL BERRY GREEN TEA SHAKER.jpeg")
        resized_image = image3.resize((100, 100))
        img3 = ImageTk.PhotoImage(resized_image)
        img3_label = tk.Label(self.order_frame, image=img3)
        img3_label.place(x=330, y=120, width=100, height=100)
        img3_label.photo = img3
        self.photos.append(img3_label)

        tea3_name = tk.Label(self.order_frame, text="GREEN TEA SHAKER", font=("Arial", 10))
        tea3_name.place(x=330, y=220, width=100, height=10)
        self.photos.append(tea3_name)
        

        teabtn3= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_tea3, state="normal")
        teabtn3.place(x=330, y=230, width=100, height=25)
        self.photos.append(teabtn3)

        # img4
        image4 = Image.open("menu_images/tea/YUZU CITRUS BLACK TEA SHAKER.jpeg")
        resized_image = image4.resize((100, 100))
        img4 = ImageTk.PhotoImage(resized_image)
        img4_label = tk.Label(self.order_frame, image=img4)
        img4_label.place(x=440, y=120, width=100, height=100)
        img4_label.photo = img4
        self.photos.append(img4_label)

        tea4_name = tk.Label(self.order_frame, text="BLACK TEA SHAKER", font=("Arial", 10))
        tea4_name.place(x=440, y=220, width=100, height=10)
        self.photos.append(tea4_name)

        teabtn4= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_tea4, state="normal")
        teabtn4.place(x=440, y=230, width=100, height=25)
        self.photos.append(teabtn4)

    def foods_show(self):
        self.clear_window()
        # img1 + btn1
        image1 = Image.open("menu_images/food/BACON BRIOCHE.jpeg")
        resized_image = image1.resize((100, 100))
        img1 = ImageTk.PhotoImage(resized_image)
        img1_label = tk.Label(self.order_frame, image=img1)
        img1_label.place(x=110, y=120, width=100, height=100)
        img1_label.photo = img1
        self.photos.append(img1_label)

        food1_name = tk.Label(self.order_frame, text="BACON BRIOCHE", font=("Arial", 10))
        food1_name.place(x=110, y=220, width=100, height=10)
        self.photos.append(food1_name)

        foodbtn1= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food1, state="normal")
        foodbtn1.place(x=110, y=230, width=100, height=25)
        self.photos.append(foodbtn1)

        # img2
        image2 = Image.open("menu_images/food/HAM & SWISS.jpeg")
        resized_image = image2.resize((100, 100))
        img2 = ImageTk.PhotoImage(resized_image)
        img2_label = tk.Label(self.order_frame, image=img2)
        img2_label.place(x=220, y=120, width=100, height=100)
        img2_label.photo = img2
        self.photos.append(img2_label)

        food2_name = tk.Label(self.order_frame, text="HAM & SWISS", font=("Arial", 10))
        food2_name.place(x=220, y=220, width=100, height=10)
        self.photos.append(food2_name)

        foodbtn2= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food2, state="normal")
        foodbtn2.place(x=220, y=230, width=100, height=25)
        self.photos.append(foodbtn2)

        # img3
        image3 = Image.open("menu_images/food/TURKEY SANDWICH.jpeg")
        resized_image = image3.resize((100, 100))
        img3 = ImageTk.PhotoImage(resized_image)
        img3_label = tk.Label(self.order_frame, image=img3)
        img3_label.place(x=330, y=120, width=100, height=100)
        img3_label.photo = img3
        self.photos.append(img3_label)

        food3_name = tk.Label(self.order_frame, text="TURKEY SANDWICH", font=("Arial", 10))
        food3_name.place(x=330, y=220, width=100, height=10)
        self.photos.append(food3_name)

        foodbtn3= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food3, state="normal")
        foodbtn3.place(x=330, y=230, width=100, height=25)
        self.photos.append(foodbtn3)

        # img4
        image4 = Image.open("menu_images/food/EGG & CHEESE.jpeg")
        resized_image = image4.resize((100, 100))
        img4 = ImageTk.PhotoImage(resized_image)
        img4_label = tk.Label(self.order_frame, image=img4)
        img4_label.place(x=440, y=120, width=100, height=100)
        img4_label.photo = img4
        self.photos.append(img4_label)

        food4_name = tk.Label(self.order_frame, text="EGG & CHEESE", font=("Arial", 10))
        food4_name.place(x=440, y=220, width=100, height=10)
        self.photos.append(food4_name)

        foodbtn4= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food4, state="normal")
        foodbtn4.place(x=440, y=230, width=100, height=25)
        self.photos.append(foodbtn4)

        # img5
        image5 = Image.open("menu_images/food/PLANT SANDWICH.jpeg")
        resized_image = image5.resize((100, 100))
        img5 = ImageTk.PhotoImage(resized_image)
        img5_label = tk.Label(self.order_frame, image=img5)
        img5_label.place(x=110, y=270, width=100, height=100)
        img5_label.photo = img5
        self.photos.append(img5_label)

        food5_name = tk.Label(self.order_frame, text="PLANT SANDWICH", font=("Arial", 10))
        food5_name.place(x=110, y=370, width=100, height=10)
        self.photos.append(food5_name)

        foodbtn5= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food5, state="normal")
        foodbtn5.place(x=110, y=380, width=100, height=25)
        self.photos.append(foodbtn5)

        # img6
        image6 = Image.open("menu_images/food/CAPRESE.jpeg")
        resized_image = image6.resize((100, 100))
        img6 = ImageTk.PhotoImage(resized_image)
        img6_label = tk.Label(self.order_frame, image=img6)
        img6_label.place(x=220, y=270, width=100, height=100)
        img6_label.photo = img6
        self.photos.append(img6_label)

        food6_name = tk.Label(self.order_frame, text="CAPRESE", font=("Arial", 10))
        food6_name.place(x=220, y=370, width=100, height=10)
        self.photos.append(food6_name)

        foodbtn6= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food6, state="normal")
        foodbtn6.place(x=220, y=380, width=100, height=25)
        self.photos.append(foodbtn6)

        # img7
        image7 = Image.open("menu_images/food/SIMPLY OATMEAL.jpeg")
        resized_image = image7.resize((100, 100))
        img7 = ImageTk.PhotoImage(resized_image)
        img7_label = tk.Label(self.order_frame, image=img7)
        img7_label.place(x=330, y=270, width=100, height=100)
        img7_label.photo = img7
        self.photos.append(img7_label)

        food7_name = tk.Label(self.order_frame, text="SIMPLY OATMEAL", font=("Arial", 10))
        food7_name.place(x=330, y=370, width=100, height=10)
        self.photos.append(food7_name)

        foodbtn7= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_food7, state="normal")
        foodbtn7.place(x=330, y=380, width=100, height=25)
        self.photos.append(foodbtn7)

    def otherbeverage_show(self):
        self.clear_window()
        # img1 + btn1
        image1 = Image.open("menu_images/other beverage/HOT COCOA.png")
        resized_image = image1.resize((100, 100))
        img1 = ImageTk.PhotoImage(resized_image)
        img1_label = tk.Label(self.order_frame, image=img1)
        img1_label.place(x=110, y=120, width=100, height=100)
        img1_label.photo = img1
        self.photos.append(img1_label)

        beverage1_name = tk.Label(self.order_frame, text="HOT COCOA", font=("Arial", 10))
        beverage1_name.place(x=110, y=220, width=100, height=10)
        self.photos.append(beverage1_name)

        beveragebtn1= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_beverage1, state="normal")
        beveragebtn1.place(x=110, y=230, width=100, height=25)
        self.photos.append(beveragebtn1)

        # img2
        image2 = Image.open("menu_images/other beverage/STEAMED MILK.png")
        resized_image = image2.resize((100, 100))
        img2 = ImageTk.PhotoImage(resized_image)
        img2_label = tk.Label(self.order_frame, image=img2)
        img2_label.place(x=220, y=120, width=100, height=100)
        img2_label.photo = img2
        self.photos.append(img2_label)

        beverage2_name = tk.Label(self.order_frame, text="STEAMED MILK", font=("Arial", 10))
        beverage2_name.place(x=220, y=220, width=100, height=10)
        self.photos.append(beverage2_name)

        beveragebtn2= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_beverage2, state="normal")
        beveragebtn2.place(x=220, y=230, width=100, height=25)
        self.photos.append(beveragebtn2)

        # img3
        image3 = Image.open("menu_images/other beverage/ICED COLA.jpeg")
        resized_image = image3.resize((100, 100))
        img3 = ImageTk.PhotoImage(resized_image)
        img3_label = tk.Label(self.order_frame, image=img3)
        img3_label.place(x=330, y=120, width=100, height=100)
        img3_label.photo = img3
        self.photos.append(img3_label)

        beverage3_name = tk.Label(self.order_frame, text="ICED COLA", font=("Arial", 10))
        beverage3_name.place(x=330, y=220, width=100, height=10)
        self.photos.append(beverage3_name)

        beveragebtn3= tk.Button(self.order_frame, text="Add", font=("Arial", 14), width=80, height=40,
                          command=self.order_beverage3, state="normal")
        beveragebtn3.place(x=330, y=230, width=100, height=25)
        self.photos.append(beveragebtn3)

    # -------------------------------------------order--------------------------------------------------
    def order_coffee1(self):
        name = "AMERICANO"
        price = 4.55
        # update total price
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        # check if the coffee item already exists in the table
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                # update the quantity and total price values for the existing row
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2)  # replace with your coffee price calculation
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            # add a new row to the table
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee2(self):
        price = 4.9
        name = "THE BLACK TIE"
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee3(self):
        price = 5.95
        name = " MACCHIATO"
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee4(self):
        price = 5.75
        name = "CAPPUCCINO"
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee5(self):
        name = "CAFFE LATTE"
        price = 5.25
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee6(self):
        name = "CAFFE MOCHA"
        price = 5.45
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee7(self):
        name = "CARAMEL FRAPPÉ"
        price = 5.95
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_coffee8(self):
        name = "ESPRESSO"
        price = 3.55
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_tea1(self):
        price = 5.35
        name = "MATCHA"
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_tea2(self):
        price = 5.25
        name = "BLACK TEA"
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_tea3(self):
        name = "GREEN TEA SHAKER"
        price = 5.90
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_tea4(self):
        name = "BLACK TEA SHAKER"
        price = 5.90
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_food1(self):
        name = "BACON BRIOCHE"
        price = 5.90
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_food2(self):
        name = "HAM & SWISS"
        price = 5.50
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_food3(self):
        name = "TURKEY SANDWICH"
        price = 5.90
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_food4(self):
        name = "EGG & CHEESE"
        price = 4.25
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_food5(self):
        name = "PLANT SANDWICH"
        price = 6.50
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_food6(self):
        name = "CAPRESE"
        price = 7.95
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))
        
    def order_food7(self):
        name = "SIMPLY OATMEAL"
        price = 3.80
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_beverage1(self):
        name = "HOT COCOA"
        price = 4.25
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_beverage2(self):
        name = "STEAMED MILK"
        price = 3.45
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))

    def order_beverage3(self):
        name = "ICED COLA"
        price = 3.25
        self.order_total += price
        self.order_total_label.config(text="Order Total: ${:.2f}".format(self.order_total))
        for row in self.table.get_children():
            values = self.table.item(row)['values']
            if values[0] == name:
                quantity = int(values[1]) + 1
                total_price = round(quantity * price, 2) 
                self.table.item(row, values=(values[0], quantity, total_price))
                break
        else:
            quantity = 1
            total_price = round(quantity * price, 2)
            self.table.insert("", "end", values=(name, quantity, total_price))