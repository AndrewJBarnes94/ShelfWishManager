import tkinter as tk
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from io import BytesIO  # Add this import
import os
import logging
import re

class LeftPane:
    def __init__(self, parent, db):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Current Book Section
        self.current_book_frame = tk.LabelFrame(self.frame, text="Current Book", bg="white")
        self.current_book_frame.pack(fill=tk.X, pady=10)
        
        self.current_book_cover_label = tk.Label(self.current_book_frame, bg="white")
        self.current_book_cover_label.pack(pady=5)
        
        self.current_book_title = tk.Label(self.current_book_frame, text="Book Title", bg="white", font=("Arial", 14))
        self.current_book_title.pack(pady=5)
        
        self.current_book_subtitle = tk.Label(self.current_book_frame, text="", bg="white", font=("Arial", 12))
        self.current_book_subtitle.pack(pady=5)
        
        self.current_book_author = tk.Label(self.current_book_frame, text="Author Name", bg="white", font=("Arial", 12))
        self.current_book_author.pack(pady=5)
        
        self.current_book_progress = ttk.Progressbar(self.current_book_frame, length=200, mode='determinate')
        self.current_book_progress['value'] = 50  # Example progress value
        self.current_book_progress.pack(pady=5)
        
        # Reading Goals Section
        self.reading_goals_frame = tk.LabelFrame(self.frame, text="2025 Reading Goals", bg="white")
        self.reading_goals_frame.pack(fill=tk.X, pady=10)
        
        self.reading_goals_progress = ttk.Progressbar(self.reading_goals_frame, length=200, mode='determinate')
        self.reading_goals_progress['value'] = 75  # Example progress value
        self.reading_goals_progress.pack(pady=5)
        
        self.reading_goals_label = tk.Label(self.reading_goals_frame, text="75% (15/20 books)", bg="white", font=("Arial", 12))
        self.reading_goals_label.pack(pady=5)
        
        # Load current book
        self.load_current_book(db)
    
    def load_current_book(self, db):
        """Load the current book being read from the database."""
        current_book = db.get_current_book()
        if current_book:
            title = current_book["title"]
            match = re.match(r"^(.*?)(\s*\(.*\))?$", title)
            main_title = match.group(1) if match else title
            subtitle = match.group(2) if match and match.group(2) else ""
            
            self.current_book_title.config(text=main_title)
            self.current_book_subtitle.config(text=subtitle)
            self.current_book_author.config(text=current_book["author"])
            
            if current_book["cover"]:
                cover_image = Image.open(BytesIO(current_book["cover"]))
                cover_image = cover_image.resize((100, 150), Image.LANCZOS)
                cover_photo = ImageTk.PhotoImage(cover_image)
                self.current_book_cover_label.config(image=cover_photo)
                self.current_book_cover_label.image = cover_photo  # Keep a reference to avoid garbage collection
            else:
                self.current_book_cover_label.config(text="No Cover", image="")
        else:
            self.current_book_title.config(text="No Current Book")
            self.current_book_subtitle.config(text="")
            self.current_book_author.config(text="")
            self.current_book_cover_label.config(text="No Cover", image="")
