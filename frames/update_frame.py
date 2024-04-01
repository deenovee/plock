import tkinter as tk
from tkinter import *
import customtkinter as ctk
from functions.g_pass import GPass
from sh import Password
import sqlite3
import datetime

class UpdateFrame(ctk.CTkFrame):
    def __init__(self, master, return_to_menu):
        self.g_pass = GPass()
        self.conn = sqlite3.connect('lockin.db')
        self.c = self.conn.cursor()
        super().__init__(master)

        self.return_to_menu = return_to_menu

        self.acct_label = ctk.CTkLabel(self, text="Account To Update:")
        self.acct_label.pack()

        self.acct_entry = ctk.CTkEntry(self)
        self.acct_entry.pack()

        self.email_label = ctk.CTkLabel(self, text="Email:")
        self.email_label.pack()

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack()

        self.code_label = ctk.CTkLabel(self, text="New code:")
        self.code_label.pack()

        self.code_entry = ctk.CTkEntry(self, show="*")
        self.code_entry.pack()

        # Checkboxes to control visibility of inputs
        self.email_var = tk.BooleanVar()
        self.email_var.set(False)
        self.email_checkbox = ctk.CTkCheckBox(self, text="Update Email", variable=self.email_var, command=self.toggle_email_entry)
        self.email_checkbox.pack()

        self.code_var = tk.BooleanVar()
        self.code_var.set(False)
        self.code_checkbox = ctk.CTkCheckBox(self, text="Update Code", variable=self.code_var, command=self.toggle_code_entry)
        self.code_checkbox.pack()

        self.update_button = ctk.CTkButton(self, text="Update", command=self.update)
        self.update_button.pack()

        # Initially hide the input fields
        self.email_label.pack_forget()
        self.email_entry.pack_forget()
        self.code_label.pack_forget()
        self.code_entry.pack_forget()

    def toggle_email_entry(self):
        if self.email_var.get():
            self.email_label.pack()
            self.email_entry.pack()
        else:
            self.email_label.pack_forget()
            self.email_entry.pack_forget()

    def toggle_code_entry(self):
        if self.code_var.get():
            self.code_label.pack()
            self.code_entry.pack()
        else:
            self.code_label.pack_forget()
            self.code_entry.pack_forget()

    def update(self):
        acct = self.acct_entry.get()
        email = self.email_entry.get() if self.email_var.get() else None
        code = self.code_entry.get() if self.code_var.get() else None

        if self.update_password(acct, email, code):
            tk.messagebox.showinfo("Success", "Password updated successfully.")
            # Call the return_to_menu function to return to the menu
            self.destroy()
            self.return_to_menu()
        else:
            tk.messagebox.showerror("Error", "Failed to update password.")

    def update_password(self, acct, email, pw):
        try:
            if acct is None or email is None or pw is None:
                old_values = self.c.execute("SELECT * FROM passwords WHERE acct = ?", (acct,)).fetchone()
                if acct is None:
                    acct = old_values[0]
                if email is None:
                    email = self.g_pass.decrypt(old_values[1])
                if pw is None:
                    pw = self.g_pass.decrypt(old_values[2])
                else:
                    pw = self.g_pass.g_pass(pw)
            self.c.execute("UPDATE passwords SET email = ?, p = ?, update_timestamp = ? WHERE acct = ?", (self.g_pass.encrypt(email), self.g_pass.encrypt(pw), datetime.datetime.now(), acct))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    