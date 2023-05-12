import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageOps
from HomePage import HomePage


class LoginPage:
    def __init__(self, root):
        self.root = root

    def setupWindow(self):
        # set up root window
        self.root.title("NU CAFE")
        # get the width and height of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # calculate the position of the main window
        x = (screen_width - 800) // 2
        y = (screen_height - 500) // 2
        # set the dimensions and position of the window
        self.root.geometry(f"800x500+{x}+{y}")

        # set the background photo of the root window
        img = Image.open("menu_images/login.jpeg")
        resized_image = ImageOps.fit(img, (800, 500), Image.ANTIALIAS) # resize and crop the image
        self.photo = ImageTk.PhotoImage(resized_image)
        # set the photo as the background of the root window
        background_label = tk.Label(self.root, image=self.photo)
        background_label.pack(fill=tk.BOTH, expand=True)
        background_label.pack_propagate(False)  # don't adjust size to fit contents
        background_label.lift()

    def run(self):
        # create two new StringVar variables to hold the username and password entered by the user
        username = tk.StringVar()
        password = tk.StringVar()

        # create a new frame to hold the login form
        login_frame = tk.Frame(self.root, bg="#f4eeef")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # create a label for the username entry box
        tk.Label(login_frame, text="UserName: ", bg="#f4eeef", relief="flat").grid(row=50, column=5, padx=5, pady=10)
        username = tk.Entry(login_frame)
        username.insert(0, "admin")
        username.grid(row=50, column=6, padx=5, pady=10)

        # create a label for the password entry box
        tk.Label(login_frame, text="PassWord: ", bg="#f4eeef", relief="flat").grid(row=51, column=5, padx=5, pady=10)
        password = tk.Entry(login_frame)
        password.insert(0,"5002")
        password.grid(row=51, column=6, padx=5, pady=10)

        def login():
            # check if both entries are not empty
            if not username.get() or not password.get():
                messagebox.showwarning(title="warning", message="Please enter both the food item and quantity.")
                return
            if username.get() == "admin" and password.get() == "5002":
                login_frame.destroy()
                # setup mainWindow ui
                self.home_page = HomePage()
                self.home_page.setup(self.root)
            else:
                messagebox.showwarning(title="Warning", message="Failed to login,check your username and password.")

        # create login and exit buttons
        tk.Button(login_frame, text="Exit", bg="#f4eeef", relief="flat", bd=0, highlightthickness=0, command=login_frame.quit).grid(row=52, column=5, padx=5, pady=10)
        tk.Button(login_frame, text="Login", bg="#f4eeef", relief="flat", bd=0, highlightthickness=0, command=login).grid(row=52, column=7, padx=10, pady=10)