import tkinter as tk
from tkinter import ttk, messagebox

class ResetPasswordForm:
    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id
        self.window = tk.Toplevel(root)
        self.window.title("Reset Password")
        
        self.frame = tk.Frame(self.window, padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)
        
        self.password_label = tk.Label(self.frame, text="New Password:")
        self.password_label.grid(row=0, column=0, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=0, column=1, pady=5)
        
        self.confirm_password_label = tk.Label(self.frame, text="Confirm Password:")
        self.confirm_password_label.grid(row=1, column=0, pady=5)
        self.confirm_password_entry = ttk.Entry(self.frame, show="*")
        self.confirm_password_entry.grid(row=1, column=1, pady=5)
        
        self.reset_button = ttk.Button(self.frame, text="Reset Password", command=self.reset_password)
        self.reset_button.grid(row=2, columnspan=2, pady=10)
    
    def reset_password(self):
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        self.db.reset_password(self.user_id, password)
        messagebox.showinfo("Success", "Password reset successfully")
        self.window.destroy()
