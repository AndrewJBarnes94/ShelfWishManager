import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from components.left_pane import LeftPane
from components.middle_pane import MiddlePane
from utils.database import Database
from utils.goodreads_import import import_goodreads_csv
from utils.search_books import search_books

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("bookshelf_app.log"),
    logging.StreamHandler()
])

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

class BookshelfApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Bookshelf App")
        self.root.state('zoomed')  # Maximize the window
        
        # Menu
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Import Goodreads CSV", command=self.import_goodreads_csv)
        self.file_menu.add_command(label="Exit", command=root.quit)
        
        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # Top Frame for icons and search bar
        self.top_frame = tk.Frame(self.root, bg="white")
        self.top_frame.pack(fill=tk.X, pady=10)
        
        # User account dropdown menu on the top left
        self.account_menu_button = ttk.Menubutton(self.top_frame, text="Account", direction="below")
        self.account_menu = tk.Menu(self.account_menu_button, tearoff=0)
        self.account_menu.add_command(label="Manage Account", command=self.manage_account)
        self.account_menu.add_command(label="Logout", command=self.logout)
        self.account_menu_button["menu"] = self.account_menu
        self.account_menu_button.pack(side=tk.LEFT, padx=10)
        
        # Central Frame for search bar and button
        self.central_frame = tk.Frame(self.top_frame, bg="white")
        self.central_frame.pack(side=tk.LEFT, expand=True)
        
        # Search bar and button in the top middle
        self.search_entry = ttk.Entry(self.central_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        self.search_button = ttk.Button(self.central_frame, text="Search", command=self.search_books)
        self.search_button.pack(side=tk.LEFT, padx=10)
        
        # Icons on the top right
        home_icon_path = "path/to/home_icon.png"
        community_icon_path = "path/to/community_icon.png"
        alerts_icon_path = "path/to/alerts_icon.png"
        
        if os.path.exists(home_icon_path):
            self.home_icon = PhotoImage(file=home_icon_path)
            self.home_button = tk.Button(self.top_frame, image=self.home_icon, bg="white", command=self.go_home)
        else:
            self.home_button = tk.Button(self.top_frame, text="Home", bg="white", command=self.go_home)
        
        if os.path.exists(community_icon_path):
            self.community_icon = PhotoImage(file=community_icon_path)
            self.community_button = tk.Button(self.top_frame, image=self.community_icon, bg="white", command=self.go_community)
        else:
            self.community_button = tk.Button(self.top_frame, text="Community", bg="white", command=self.go_community)
        
        if os.path.exists(alerts_icon_path):
            self.alerts_icon = PhotoImage(file=alerts_icon_path)
            self.alerts_button = tk.Button(self.top_frame, image=self.alerts_icon, bg="white", command=self.go_alerts)
        else:
            self.alerts_button = tk.Button(self.top_frame, text="Alerts", bg="white", command=self.go_alerts)
        
        self.home_button.pack(side=tk.RIGHT, padx=10)
        self.community_button.pack(side=tk.RIGHT, padx=10)
        self.alerts_button.pack(side=tk.RIGHT, padx=10)
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize database
        self.db = Database()
        
        # Initialize panes
        self.left_pane = LeftPane(self.main_frame, self.db)
        self.middle_pane = MiddlePane(self.main_frame)
        self.middle_pane.db = self.db  # Pass the db instance to MiddlePane
        
        # Books data
        self.books = []
        self.load_books()
        self.middle_pane.render_bookshelf(self.books)
    
    def import_goodreads_csv(self):
        import_goodreads_csv(self.root, self.db, self.books, self.middle_pane)
    
    def search_books(self):
        search_books(self.search_entry, self.books, self.middle_pane, self.db)
    
    def load_books(self):
        self.books = self.db.load_books()
    
    def show_about(self):
        messagebox.showinfo("About", "Bookshelf App v1.0")

    def go_home(self):
        messagebox.showinfo("Home", "Home button clicked")

    def go_community(self):
        messagebox.showinfo("Community", "Community button clicked")

    def go_alerts(self):
        messagebox.showinfo("Alerts", "Alerts button clicked")
    
    def manage_account(self):
        messagebox.showinfo("Manage Account", "Manage Account button clicked")
    
    def logout(self):
        self.root.destroy()
        main()

def on_login_success(user_id):
    login_form.root.destroy()
    root = tk.Tk()
    app = BookshelfApp(root, user_id)
    root.mainloop()

def main():
    root = tk.Tk()
    global login_form
    login_form = LoginForm(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
