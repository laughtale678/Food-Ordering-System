import tkinter as tk
from LoginPage import LoginPage


class NuCafe:
    def __init__(self):
        root = tk.Tk()
        root.geometry("800x500")
        login = LoginPage(root)  # creat an object of class 'login_page'
        login.setupWindow() 
        login.run()

        root.mainloop()


nuCafeMain = NuCafe()
