import os
import pandas as pd
from PIL import ImageTk, Image, ImageOps
import tkinter as tk
import tkinter.ttk as ttk


class ViewOrders:
    def view_order(self):
        view_frame = tk.Frame()
        view_frame.place(relx=0.5, rely=0.5, anchor="center")

        # set background picture
        img = Image.open("menu_images/homepage.jpeg")
        resized_image = ImageOps.fit(img, (800, 500), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(resized_image)
        background_label = tk.Label(view_frame, image=self.photo) # set the photo as the background of the home frame
        background_label.pack(fill=tk.BOTH, expand=True)
        background_label.pack_propagate(False) # don't adjust size to fit contents
        background_label.lift()

        # load the CSV file into a pandas DataFrame
        current_path = os.getcwd()
        df = pd.read_csv(f"{current_path}/order_data.csv")

        # create a Treeview widget with columns for each column in the DataFrame
        treeview = ttk.Treeview(view_frame, columns=list(df.columns), show="headings")
        treeview.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.8, anchor='center')

        # add headings to the Treeview widget
        for col, width in zip(df.columns, [10, 80, 350, 10]):
            treeview.heading(col, text=col)
            treeview.column(col, width=width)

        # add rows to the Treeview widget
        for index, row in df.iloc[::-1].iterrows():
            values = list(row)
            treeview.insert("", "end", values=values)

        # creat a return button
        def back():
            view_frame.destroy()

        # set button style
        style = ttk.Style()
        style.configure("RoundedButton.TButton", font=("Arial", 12, "bold"), borderwidth=0, padding=0, relief="flat", width=60, height=30)
        style.map("RoundedButton.TButton", background=[("active", "white")], foreground=[("active", "#c29060")])

        back_btn = ttk.Button(view_frame, text="Back", style="RoundedButton.TButton", command=back, state="normal")
        back_btn.place(relx=0.05, rely=0.04, width=80, height=25)

