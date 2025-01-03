import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import os
import logging
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

class BookshelfApp:
    def __init__(self, root):
        self.root = root
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
        
        # Circle icon on the top left
        circle_icon_path = "path/to/circle_icon.png"
        if os.path.exists(circle_icon_path):
            self.circle_icon = PhotoImage(file=circle_icon_path)
            self.circle_label = tk.Label(self.top_frame, image=self.circle_icon, bg="white")
        else:
            self.circle_label = tk.Label(self.top_frame, text="O", bg="white", font=("Arial", 24))
        self.circle_label.pack(side=tk.LEFT, padx=10)
        
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

if __name__ == "__main__":
    root = tk.Tk()
    app = BookshelfApp(root)
    root.mainloop()
