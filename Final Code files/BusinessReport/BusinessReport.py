import os
import pandas as pd
from PIL import ImageTk, Image, ImageOps
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BusinessReport:

    def __init__(self):
        self.temp_save = []  # store temporary frame

    def report(self):
        report_frame = tk.Frame()
        report_frame.place(relx=0.5, rely=0.5, anchor='center')

        # set background picture
        img1 = Image.open("menu_images/homepage.jpeg")
        resized_image1 = ImageOps.fit(img1, (800, 500), Image.ANTIALIAS)
        self.photo1 = ImageTk.PhotoImage(resized_image1)
        background_label1 = tk.Label(report_frame, image=self.photo1)  # set the photo as the background of the report frame
        background_label1.pack(fill=tk.BOTH, expand=True)
        background_label1.pack_propagate(False)  # don't adjust size to fit contents
        background_label1.lift()

        # set button style
        style = ttk.Style()
        style.configure("RoundedButton.TButton", font=("Arial", 12, "bold"), borderwidth=0, padding=0,
                            relief="flat", width=60, height=40, )
        style.map("RoundedButton.TButton", background=[("active", "white")], foreground=[("active", "#c29060")])

        # creat a return method
        def back():
            report_frame.destroy()

        # clear all the frame in temp_save
        def clear_window():
            for item in self.temp_save:
                item.destroy()
            self.temp_save = []

        def sales_report():
            sales_frame = tk.Frame()
            sales_frame.place(relx=0.5, rely=0.5, anchor='center')

            # set background picture
            img = Image.open("menu_images/homepage.jpeg")
            resized_image = ImageOps.fit(img, (800, 500), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(sales_frame, image=self.photo)  # set the photo as the background of the salses frame
            background_label.pack(fill=tk.BOTH, expand=True)
            background_label.pack_propagate(False)  # don't adjust size to fit contents
            background_label.lift()

            # --------------------------------------Sales Table------------------------------------------
            # create a new frame for sales table
            sales_r = tk.Frame(sales_frame, highlightthickness=0, width=600, height=350)
            sales_r.place(relx=0.5, rely=0.45, anchor='center')
            # load the CSV file into a pandas DataFrame
            current_path = os.getcwd()
            df = pd.read_csv(f"{current_path}/order_data.csv")
            # convert the Date column to a datetime object
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            # group the orders by date and calculate the sum of the order total for each date
            grouped_df = df.groupby(df['Date']).agg({'Order Number': 'count', 'Order Total': 'sum'})
            # rename the columns
            grouped_df = grouped_df.rename(columns={'Order Number': 'Order Count', 'Order Total': 'Sales Revenue'})
            grouped_df['Sales Revenue'] = grouped_df['Sales Revenue'].round(2)
            # insert the Date column as the first column
            grouped_df = grouped_df.reset_index()
            # sort the df
            grouped_df = grouped_df.sort_values(by='Date', ascending=False)
            # create another df later used to generate charts
            chart_df = grouped_df.head(7)

            # create a Treeview widget with columns for each column in the DataFrame
            treeview = ttk.Treeview(sales_r, columns=list(grouped_df.columns), show="headings")
            treeview.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
            # add headings to the Treeview widget
            for col, width in zip(grouped_df.columns, [100, 100, 100]):
                treeview.heading(col, text=col)
                treeview.column(col, width=width)
            # add rows to the Treeview widget
            for index, row in grouped_df.iterrows():
                values = list(row)
                treeview.insert("", "end", values=values)

            # ----------------------------------Total Sales label--------------------------------------
            total_sales = df['Order Total'].sum()
            order_total_label = tk.Label(sales_r, text="Sales Total: $0")
            order_total_label.place(relx=0.77, rely=0.9)
            order_total_label.config(text=f"Sales Total: ${total_sales:.2f}")

            self.temp_save.append(sales_r)

            # ---------------------- Return Button for Sales Report Page-------------------------------
            def sales_frame_back():
                sales_frame.destroy()

            # --------------------------------show Sales Detail Table-----------------------------------
            def sales_detail():
                clear_window()
                sales_r = tk.Frame(sales_frame, highlightthickness=0, width=600, height=350)
                sales_r.place(relx=0.5, rely=0.45, anchor='center')
                # load the CSV file into a pandas DataFrame
                df = pd.read_csv(f"{current_path}/order_data.csv")
                # convert the Date column to a datetime object
                df['Date'] = pd.to_datetime(df['Date']).dt.date
                # group the orders by date and calculate the sum of the order total for each date
                grouped_df = df.groupby(df['Date']).agg({'Order Number': 'count', 'Order Total': 'sum'})
                # rename the columns
                grouped_df = grouped_df.rename(columns={'Order Number': 'Order Count', 'Order Total': 'Sales Revenue'})
                grouped_df['Sales Revenue'] = grouped_df['Sales Revenue'].round(2)
                # insert the Date column as the first column
                grouped_df = grouped_df.reset_index()
                # sort the df
                grouped_df = grouped_df.sort_values(by='Date', ascending=False)
                # create another df later used to generate charts
                chart_df = grouped_df.head(7)

                # create a Treeview widget with columns for each column in the DataFrame
                treeview = ttk.Treeview(sales_r, columns=list(grouped_df.columns), show="headings")
                treeview.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor='center')
                # add headings to the Treeview widget
                for col, width in zip(grouped_df.columns, [100, 100, 100]):
                    treeview.heading(col, text=col)
                    treeview.column(col, width=width)
                # add rows to the Treeview widget
                for index, row in grouped_df.iterrows():
                    values = list(row)
                    treeview.insert("", "end", values=values)

                # ---------------------------------Total Sales label-----------------------------------
                total_sales = df['Order Total'].sum()
                order_total_label = tk.Label(sales_r, text="Sales Total: $0")
                order_total_label.place(relx=0.77, rely=0.9)
                order_total_label.config(text=f"Sales Total: ${total_sales:.2f}")
                # save current frame to temp_save
                self.temp_save.append(sales_r)

            # -----------------------------------show Sales Chart---------------------------------------
            def order_chart():
                clear_window()
                sales_f = tk.Frame(sales_frame, highlightthickness=0, width=600, height=350)
                sales_f.place(relx=0.5, rely=0.45, anchor='center')

                # create the plot using Matplotlib
                fig, ax = plt.subplots()
                fig.subplots_adjust(left=0.15, right=0.9, bottom=0.4, top=0.9)
                fig.set_size_inches(6, 4)

                ax.plot(chart_df['Date'], chart_df['Order Count'])
                ax.set_xlabel('Date')
                ax.tick_params(axis='x', labelsize=6, labelrotation=80)
                ax.set_ylabel('Order Count')
                ax.set_title('7 days Report')

                # add a canvas to display the plot
                canvas = FigureCanvasTkAgg(fig, master=sales_f)
                canvas.draw()
                canvas_width = canvas.get_tk_widget().winfo_width()
                canvas_height = canvas.get_tk_widget().winfo_height()
                canvas_x = (sales_f.winfo_width() - canvas_width) // 2
                canvas_y = (sales_f.winfo_height() - canvas_height) // 2
                canvas.get_tk_widget().place(x=canvas_x, y=canvas_y)

                self.temp_save.append(sales_f)

            # -----------------------------------show Order Chart---------------------------------------
            def sales_chart():
                clear_window()
                order_f = tk.Frame(sales_frame, highlightthickness=0, width=600, height=350)
                order_f.place(relx=0.5, rely=0.45, anchor='center')

                # create the plot using Matplotlib
                fig, ax = plt.subplots()
                fig.subplots_adjust(left=0.15, right=0.9, bottom=0.4, top=0.9)
                fig.set_size_inches(6, 4)

                ax.plot(chart_df['Date'], chart_df['Sales Revenue'])
                ax.set_xlabel('Date')
                ax.tick_params(axis='x', labelsize=6, labelrotation=80)
                ax.set_ylabel('Sales Revenue')
                ax.set_title('7 days Report')

                # add a canvas to display the plot
                canvas = FigureCanvasTkAgg(fig, master=order_f)
                canvas.draw()
                canvas_width = canvas.get_tk_widget().winfo_width()
                canvas_height = canvas.get_tk_widget().winfo_height()
                canvas_x = (order_f.winfo_width() - canvas_width) // 2
                canvas_y = (order_f.winfo_height() - canvas_height) // 2
                canvas.get_tk_widget().place(x=canvas_x, y=canvas_y)

                self.temp_save.append(order_f)
            
            # set buttons
            back_btn = ttk.Button(sales_frame, text="Back", style='RoundedButton.TButton', command=sales_frame_back,
                                  state="normal")
            back_btn.place(relx=0.14, rely=0.85, width=100, height=25)

            sales_detail_btn = ttk.Button(sales_frame, text="Sales Report", style='RoundedButton.TButton', command=sales_detail,
                                  state="normal")
            sales_detail_btn.place(relx=0.34, rely=0.85, width=100, height=25)

            order_chart_btn = ttk.Button(sales_frame, text="Order Chart", style='RoundedButton.TButton', command=order_chart,
                                  state="normal")
            order_chart_btn.place(relx=0.54, rely=0.85, width=100, height=25)

            order_btn = ttk.Button(sales_frame, text="Sales Chart", style='RoundedButton.TButton', command=sales_chart,
                                  state="normal")
            order_btn.place(relx=0.74, rely=0.85, width=100, height=25)

        def product_report():
            product_frame = tk.Frame()
            product_frame.place(relx=0.5, rely=0.5, anchor='center')

            # set background picture
            current_path = os.getcwd()
            img = Image.open(f"{current_path}/menu_images/homepage.jpeg")
            resized_image = ImageOps.fit(img, (800, 500), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(resized_image)
            background_label = tk.Label(product_frame, image=self.photo)  # set the photo as the background of the product frame
            background_label.pack(fill=tk.BOTH, expand=True)
            background_label.pack_propagate(False)  # don't adjust size to fit contents
            background_label.lift()

            # load the CSV file into a pandas DataFrame
            df = pd.read_csv(f"{current_path}/item_counts.csv")

            # create the plot using Matplotlib
            fig, ax = plt.subplots()
            fig.subplots_adjust(left=0.15, right=0.9, bottom=0.4, top=0.9)

            ax.bar(df['Item Name'], df['Quantity Sold'])
            ax.set_xlabel('Item Name')
            ax.tick_params(axis='x', labelsize=6, labelrotation=80)
            ax.set_ylabel('Quantity Sold')
            ax.set_title('Product Report')

            # add a canvas to display the plot
            canvas = FigureCanvasTkAgg(fig, master=product_frame)
            canvas.draw()
            # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center')

            # creat a return button
            def product_frame_back():
                product_frame.destroy()

            back_btn = ttk.Button(product_frame, text="Back", style='RoundedButton.TButton', command=product_frame_back,
                                  state="normal")
            back_btn.place(x=0, y=12, width=80, height=25)

#---------------------------------------------set buttons----------------------------------------------------
        def btn(x, y, text, bcolor, fcolor, cmd):

            def on_enter(e):
                mybtn['background']=bcolor
                mybtn['foreground']=fcolor

            def on_leave(e):
                mybtn['background']=fcolor
                mybtn['foreground']=bcolor

            mybtn = tk.Button(report_frame,width=24, height=2,text=text,font=('Arial', 15, 'bold'),
                              fg=bcolor,
                              bg=fcolor,
                              highlightthickness=0,
                              relief='flat', 
                              borderwidth=0,
                              activeforeground=fcolor,
                              activebackground=bcolor,
                              command=cmd)
            mybtn.bind("<Enter>", on_enter)
            mybtn.bind("<Leave>", on_leave)

            mybtn.place(x=x, y=y)

        btn(280, 150, "Sales Report", "black", "#c29060", sales_report)
        btn(280, 220, "Product Report", "black", "#c29060", product_report)
        btn(280, 290, "Back", "black", "#c29060", back)




