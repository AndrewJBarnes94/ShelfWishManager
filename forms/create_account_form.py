import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class CreateAccountForm:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.window = tk.Toplevel(root)
        self.window.title("Create Account")
        
        self.frame = tk.Frame(self.window, padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)
        
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, pady=5)
        
        self.email_label = tk.Label(self.frame, text="Email:")
        self.email_label.grid(row=1, column=0, pady=5)
        self.email_entry = ttk.Entry(self.frame)
        self.email_entry.grid(row=1, column=1, pady=5)
        
        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        self.create_button = ttk.Button(self.frame, text="Create Account", command=self.create_account)
        self.create_button.grid(row=3, columnspan=2, pady=10)
    
    def create_account(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            self.db.create_user(username, email, password)
            messagebox.showinfo("Success", "Account created successfully")
            self.window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")
