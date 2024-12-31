import tkinter as tk
from tkinter import ttk, PhotoImage
import os

class LeftPane:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Current Book Section
        self.current_book_frame = tk.LabelFrame(self.frame, text="Current Book", bg="white")
        self.current_book_frame.pack(fill=tk.X, pady=10)
        
        book_cover_path = "path/to/book_cover.png"
        if os.path.exists(book_cover_path):
            self.current_book_cover = PhotoImage(file=book_cover_path)
            self.current_book_cover_label = tk.Label(self.current_book_frame, image=self.current_book_cover, bg="white")
        else:
            self.current_book_cover_label = tk.Canvas(self.current_book_frame, width=100, height=150, bg="white")
            self.current_book_cover_label.create_rectangle(10, 10, 90, 140, outline="black", fill="lightgray")
            self.current_book_cover_label.create_text(50, 75, text="No Cover", font=("Arial", 12))
        self.current_book_cover_label.pack(pady=5)
        
        self.current_book_title = tk.Label(self.current_book_frame, text="Book Title", bg="white", font=("Arial", 14))
        self.current_book_title.pack(pady=5)
        
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
