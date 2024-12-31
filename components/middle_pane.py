import tkinter as tk
from PIL import Image, ImageTk, UnidentifiedImageError
from io import BytesIO
import logging

class MiddlePane:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.cover_photos = []  # Keep references to cover photos to avoid garbage collection
        
        # Pagination controls
        self.current_page = 0
        self.books_per_page = 75  # Number of books per page (15 books per shelf * 5 shelves)
        
        self.pagination_frame = tk.Frame(self.frame, bg="white")
        self.pagination_frame.pack(fill=tk.X, pady=10)
        
        self.prev_button = tk.Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        
        self.page_label = tk.Label(self.pagination_frame, text="Page 1", bg="white")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        self.next_button = tk.Button(self.pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        # Bind the configure event to handle resizing
        self.canvas.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        """Handle the resizing of the canvas."""
        self.show_page(self.current_page)
    
    def render_bookshelf(self, books):
        """Render the books on the bookshelf."""
        self.books = books
        self.total_pages = (len(books) + self.books_per_page - 1) // self.books_per_page  # Calculate total pages
        self.show_page(self.current_page)
    
    def show_page(self, page):
        """Show the specified page of books."""
        self.canvas.delete("all")  # Clear previous drawings
        self.cover_photos.clear()  # Clear previous references
        
        # Get the current width and height of the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Ensure minimum canvas size
        if canvas_width < 100 or canvas_height < 100:
            logging.warning("Canvas size too small to render bookshelf.")
            return
        
        # Draw bookshelf background
        self.canvas.create_rectangle(50, 20, canvas_width - 50, canvas_height - 80, fill="#DEB887", outline="black")
        
        # Draw shelves
        shelf_height = (canvas_height - 100) // 5
        for i in range(1, 6):
            self.canvas.create_line(50, i * shelf_height + 20, canvas_width - 50, i * shelf_height + 20, width=4, fill="#8B4513")
        
        # Draw books
        start_index = page * self.books_per_page
        end_index = min(start_index + self.books_per_page, len(self.books))
        book_width = max((canvas_width - 100) // 15, 1)
        book_height = max(shelf_height - 20, 1)
        for index, book in enumerate(self.books[start_index:end_index]):
            x0 = 60 + (index % 15) * book_width
            y0 = (index // 15) * shelf_height + 30
            x1 = x0 + book_width - 10
            y1 = y0 + book_height
            
            # Draw book cover if available
            if book.get("cover"):
                try:
                    cover_image = Image.open(BytesIO(book["cover"]))
                    cover_image = cover_image.resize((book_width - 10, book_height), Image.LANCZOS)
                    cover_photo = ImageTk.PhotoImage(cover_image)
                    self.canvas.create_image(x0 + (book_width - 10) // 2, y0 + book_height // 2, image=cover_photo)
                    self.cover_photos.append(cover_photo)  # Keep a reference to avoid garbage collection
                    logging.info(f"Rendered cover for {book['title']}")
                except UnidentifiedImageError as e:
                    logging.error(f"Failed to render cover for {book['title']}: {e}")
            else:
                # Draw book
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", outline="black")
                self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=book["title"], width=book_width - 20)
        
        # Update pagination controls
        self.page_label.config(text=f"Page {self.current_page + 1} of {self.total_pages}")
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED)
    
    def prev_page(self):
        """Go to the previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)
    
    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_page(self.current_page)
