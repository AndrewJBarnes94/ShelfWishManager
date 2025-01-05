import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import os
import logging
from components.left_pane import LeftPane
from components.middle_pane import MiddlePane
from utils.database import Database
from utils.goodreads_import import import_goodreads_csv
from utils.search_books import search_books
from forms.login_form import LoginForm
from forms.create_account_form import CreateAccountForm
from forms.recover_password_form import RecoverPasswordForm
from forms.reset_password_form import ResetPasswordForm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("bookshelf_app.log"),
    logging.StreamHandler()
])

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
        self.left_pane = LeftPane(self.main_frame, self.db, self.user_id)
        self.middle_pane = MiddlePane(self.main_frame)
        self.middle_pane.db = self.db  # Pass the db instance to MiddlePane
        
        # Books data
        self.books = []
        self.load_books()
        self.middle_pane.render_bookshelf(self.books)
    
    def import_goodreads_csv(self):
        import_goodreads_csv(self.root, self.db, self.books, self.middle_pane, self.user_id)
    
    def search_books(self):
        search_books(self.search_entry, self.books, self.middle_pane, self.db, self.user_id)
    
    def load_books(self):
        self.books = self.db.load_books(self.user_id)
    
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
