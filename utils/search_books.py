import requests
import tkinter as tk
from tkinter import Toplevel, Listbox, messagebox, ttk

def search_books(search_entry, books, middle_pane):
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
            
            # Fetch and save cover image
            cover_image = None
            if cover_url:
                cover_response = requests.get(cover_url)
                cover_image = cover_response.content
            
            books.append({"title": title, "author": author, "cover": cover_image})
            middle_pane.render_bookshelf(books)
            search_results_window.destroy()
        
        save_button = ttk.Button(search_results_window, text="Save", command=save_book)
        save_button.pack(pady=10)
            
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch books: {e}")
