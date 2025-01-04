import requests
import tkinter as tk
from tkinter import Toplevel, Listbox, messagebox, ttk
from io import BytesIO
import uuid

def search_books(search_entry, books, middle_pane, db):
    """Search books using OpenLibrary API and show results in a new window."""
    query = search_entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a search term.")
        return
    
    url = f"https://openlibrary.org/search.json?q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Create a new Toplevel window for search results
        search_results_window = Toplevel()
        search_results_window.title("Search Results")
        
        results_list = Listbox(search_results_window, width=100, height=20)
        results_list.pack(pady=10)
        
        book_details = {}  # Dictionary to store book details
        
        for book in data.get("docs", [])[:10]:  # Limit results to 10
            title = book.get("title", "No Title")
            author = ", ".join(book.get("author_name", ["Unknown Author"]))
            cover_id = book.get("cover_i")
            cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None
            book_id = f"{title} by {author}"
            book_details[book_id] = {"title": title, "author": author, "cover_url": cover_url}
            results_list.insert(tk.END, book_id)
        
        def save_book():
            selected = results_list.curselection()
            if not selected:
                messagebox.showerror("Error", "No book selected.")
                return
            
            book_id = results_list.get(selected[0])
            book_info = book_details[book_id]
            title, author, cover_url = book_info["title"], book_info["author"], book_info["cover_url"]
            
            # Check for duplicates
            if any(book['title'] == title and book['author'] == author for book in books):
                messagebox.showwarning("Duplicate Entry", f"The book '{title}' by {author} is already in your collection.")
                return
            
            # Fetch and save cover image
            cover_image = None
            if cover_url:
                cover_response = requests.get(cover_url)
                cover_image = cover_response.content
            
            new_book = {
                "book_id": str(uuid.uuid4()),  # Generate a unique book_id
                "title": title,
                "author": author,
                "author_lf": None,
                "additional_authors": None,
                "isbn": None,
                "isbn13": None,
                "my_rating": None,
                "average_rating": None,
                "publisher": None,
                "binding": None,
                "number_of_pages": None,
                "year_published": None,
                "original_publication_year": None,
                "date_read": None,
                "date_added": None,
                "bookshelves": None,
                "bookshelves_with_positions": None,
                "exclusive_shelf": None,
                "my_review": None,
                "spoiler": None,
                "private_notes": None,
                "read_count": None,
                "owned_copies": None,
                "cover": cover_image
            }
            
            books.append(new_book)
            db.save_books(books)
            middle_pane.render_bookshelf(books)
            search_results_window.destroy()
        
        save_button = ttk.Button(search_results_window, text="Save", command=save_book)
        save_button.pack(pady=10)
            
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch books: {e}")
