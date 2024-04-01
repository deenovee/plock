import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3

class DeleteFrame(ctk.CTkFrame):
    def __init__(self, master, return_to_menu):
        self.conn = sqlite3.connect('lockin.db')
        self.c = self.conn.cursor()
        super().__init__(master)
        self.return_to_menu = return_to_menu  # Save return_to_menu function

        self.acct_label = ctk.CTkLabel(self, text="Account Name:")
        self.acct_label.pack()

        self.acct_entry = ctk.CTkEntry(self)
        self.acct_entry.pack()

        self.delete_button = ctk.CTkButton(self, text="Delete", command=self.delete)
        self.delete_button.pack()

    def delete(self):
        acct = self.acct_entry.get()
        if self.delete_password(acct):
            messagebox.showinfo("Success", "Account Deleted Successfully")
            self.destroy()
            # Call the return_to_menu function to return to the menu
            self.return_to_menu()
        else:
            messagebox.showerror("Error", "Failed to delete password.")

    def delete_password(self, acct):
        try:
            self.c.execute("DELETE FROM passwords WHERE acct = ?", (acct,))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
