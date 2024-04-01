from tkinter import messagebox
import customtkinter as ctk
from frames.view_frame import ViewFrame
from frames.add_frame import AddFrame
from frames.update_frame import UpdateFrame
from frames.delete_frame import DeleteFrame
import sqlite3

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.conn = sqlite3.connect('lockin.db')
        self.c = self.conn.cursor()
        self._appearance = ctk.set_appearance_mode("dark")
        self._color = ctk.set_default_color_theme("blue")

        self.crud_label = ctk.CTkLabel(self, text="C, R, U, D, exit: (1/2/3/4/5)")
        self.crud_label.pack()

        self.crud_entry = ctk.CTkEntry(self)
        self.crud_entry.pack()

        self.crud_button = ctk.CTkButton(self, text="Submit", command=self.process_input)
        self.crud_button.pack()

    def process_input(self):
        choice = self.crud_entry.get()
        if choice == "1":
            self.add_password()
        elif choice == "2":
            self.view_passwords()
        elif choice == "3":
            self.update_password()
        elif choice == "4":
            self.delete_password()
        elif choice == "5":
            self.master.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid choice (1/2/3/4/5)")
        
    def add_password(self):
        self.destroy()
        self.add_frame = AddFrame(self.master, self.return_to_menu)
        self.add_frame.pack()

    def view_passwords(self):
        self.destroy()
        passwords = self.retrieve_passwords()
        if passwords:
            self.view_frame = ViewFrame(self.master, passwords, return_to_menu=self.return_to_menu)
            self.view_frame.pack()
        else:
            messagebox.showinfo("No Accounts", "No accounts found.")
    
    def update_password(self):
        self.destroy()
        self.update_frame = UpdateFrame(self.master, self.return_to_menu)
        self.update_frame.pack()
    
    def delete_password(self):
        self.destroy()
        self.delete_frame = DeleteFrame(self.master, self.return_to_menu)
        self.delete_frame.pack()

    def retrieve_passwords(self):
        try:
            accounts = self.c.execute("SELECT acct, email, p, update_timestamp FROM passwords").fetchall()
            return accounts
        except Exception as e:
            print(e)
            return None
    
    def return_to_menu(self):
        self.destroy()
        new_menu_frame = MenuFrame(self.master)
        new_menu_frame.pack()