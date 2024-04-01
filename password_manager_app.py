from tkinter import messagebox
import customtkinter as ctk
from frames.menu_frame import MenuFrame
import bcrypt
from functions.load_variables import Variables

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.variables = Variables() 
        self.appearance = ctk.set_appearance_mode("dark")
        self.color = ctk.set_default_color_theme("blue") 

        self.title("Password Manager")

        self.passphrase_label = ctk.CTkLabel(self, text="Enter passphrase to begin:")
        self.passphrase_label.pack()

        self.passphrase_entry = ctk.CTkEntry(self, show="*")
        self.passphrase_entry.pack()

        self.access_button = ctk.CTkButton(self, text="Access", command=self.access_manager)
        self.access_button.pack()

    def access_manager(self):
        passphrase = self.passphrase_entry.get()
        if self.check_passphrase(passphrase):
            self.passphrase_label.destroy()
            self.passphrase_entry.destroy()
            self.access_button.destroy()

            self.menu_frame = MenuFrame(self)
            self.menu_frame.pack()
        else:
            messagebox.showerror("Access Denied", "Incorrect passphrase")

    def check_passphrase(self, passphrase):
        p_phrase = self.variables.check_passphrase()
        if bcrypt.checkpw(passphrase.encode(), p_phrase):
            return True
        else:
            return False