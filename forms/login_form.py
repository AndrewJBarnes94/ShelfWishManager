import tkinter as tk
from tkinter import ttk, messagebox
from utils.database import Database
from forms.create_account_form import CreateAccountForm
from forms.recover_password_form import RecoverPasswordForm
from forms.reset_password_form import ResetPasswordForm

class LoginForm:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()
        self.root.title("Login")
        
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)
        
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, pady=5)
        
        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        self.login_button = ttk.Button(self.frame, text="Login", command=self.check_credentials)
        self.login_button.grid(row=2, columnspan=2, pady=10)
        
        self.create_account_button = ttk.Button(self.frame, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=3, columnspan=2, pady=5)
        
        self.recover_password_button = ttk.Button(self.frame, text="Recover Password", command=self.recover_password)
        self.recover_password_button.grid(row=4, columnspan=2, pady=5)
    
    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user_id, is_temp_token = self.db.authenticate_user(username, password)
        if user_id:
            if is_temp_token:
                self.on_temp_token_login(user_id)
            else:
                self.on_login_success(user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def create_account(self):
        CreateAccountForm(self.root, self.db)
    
    def recover_password(self):
        RecoverPasswordForm(self.root, self.db)
    
    def on_temp_token_login(self, user_id):
        ResetPasswordForm(self.root, self.db, user_id)
