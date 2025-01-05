import tkinter as tk
from tkinter import ttk, messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class RecoverPasswordForm:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.window = tk.Toplevel(root)
        self.window.title("Recover Password")
        
        self.frame = tk.Frame(self.window, padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)
        
        self.email_label = tk.Label(self.frame, text="Email:")
        self.email_label.grid(row=0, column=0, pady=5)
        self.email_entry = ttk.Entry(self.frame)
        self.email_entry.grid(row=0, column=1, pady=5)
        
        self.recover_button = ttk.Button(self.frame, text="Recover Password", command=self.recover_password)
        self.recover_button.grid(row=1, columnspan=2, pady=10)
    
    def recover_password(self):
        email = self.email_entry.get()
        
        if not email:
            messagebox.showerror("Error", "Email is required")
            return
        
        user = self.db.get_user_by_email(email)
        if user:
            temp_token = self.db.create_temp_token(user["id"])
            self.send_recovery_email(email, user["username"], temp_token)
            messagebox.showinfo("Password Recovery", f"Password recovery instructions have been sent to {email}")
        else:
            messagebox.showerror("Error", "No account found with that email address")
    
    def send_recovery_email(self, email, username, temp_token):
        """Send a password recovery email."""
        sender_email = "andrew.barnes@brocodesoftware.com"
        sender_password = "Qwertyuiop1313!"
        subject = "Password Recovery Instructions"
        body = f"Hello {username},\n\nTo reset your password, please use the following temporary password to log in:\n\nTemporary Password: {temp_token}\n\nBest regards,\nBookshelf App Team"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP('smtp.privateemail.com', 587)  # Replace with your SMTP server and port
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            server.quit()
            logging.info(f"Password recovery email sent to {email}")
        except Exception as e:
            logging.error(f"Failed to send password recovery email to {email}: {e}")
