import csv
import requests
import logging
import time
import threading
from tkinter import filedialog, Toplevel, Label, ttk
from queue import Queue

def find_isbn(title, author):
    """Find ISBN using Google Books API."""
    query = f"{title} {author}"
    url_google_books = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    try:
        response = requests.get(url_google_books)
        response.raise_for_status()
        data = response.json()
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            industry_identifiers = volume_info.get("industryIdentifiers", [])
            for identifier in industry_identifiers:
                if identifier.get("type") in ["ISBN_10", "ISBN_13"]:
                    isbn = identifier.get("identifier")
                    logging.info(f"Found ISBN for {title} using Google Books: {isbn}")
                    return isbn
        time.sleep(1)  # Add delay to avoid hitting rate limit
    except requests.RequestException as e:
        logging.error(f"Failed to find ISBN for {title} using Google Books: {e}")
    return None

def find_cover_image(isbn, isbn13, title, author):
    """Find cover image using Google Books API and OpenLibrary API as a fallback."""
    queries = []
    if isbn:
        queries.append(f"isbn:{isbn}")
    if isbn13:
        queries.append(f"isbn:{isbn13}")
    queries.append(f"{title} {author}")
    
    for query in queries:
        url_google_books = f"https://www.googleapis.com/books/v1/volumes?q={query}"
        try:
            response = requests.get(url_google_books)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                volume_info = item.get("volumeInfo", {})
                cover_url = volume_info.get("imageLinks", {}).get("thumbnail")
                if cover_url:
                    cover_response = requests.get(cover_url, timeout=10)
                    cover_response.raise_for_status()
                    logging.info(f"Fetched cover for {title} using Google Books with query: {query}")
                    return cover_response.content
            time.sleep(1)  # Add delay to avoid hitting rate limit
        except requests.RequestException as e:
            logging.error(f"Failed to fetch cover for {title} using Google Books with query: {query}: {e}")
    
    # Fallback to OpenLibrary API
    for query in queries:
        url_openlibrary = f"https://openlibrary.org/search.json?q={query}"
        try:
            response = requests.get(url_openlibrary)
            response.raise_for_status()
            data = response.json()
            for doc in data.get("docs", []):
                cover_id = doc.get("cover_i")
                if cover_id:
                    cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                    cover_response = requests.get(cover_url, timeout=10)
                    cover_response.raise_for_status()
                    logging.info(f"Fetched cover for {title} using OpenLibrary with query: {query}")
                    return cover_response.content
            time.sleep(1)  # Add delay to avoid hitting rate limit
        except requests.RequestException as e:
            logging.error(f"Failed to fetch cover for {title} using OpenLibrary with query: {query}: {e}")
    return None

def import_goodreads_csv(root, db, books, middle_pane, user_id):
    """Import books from a Goodreads CSV file."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    
    # Create a progress bar window
    progress_window = Toplevel()
    progress_window.title("Importing CSV")
    progress_label = Label(progress_window, text="Importing books...")
    progress_label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
    progress_bar.pack(pady=10)
    
    # Calculate total number of rows
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        total_rows = sum(1 for row in reader) - 1  # Subtract 1 for header row
    
    progress_bar['maximum'] = total_rows
    
    def process_csv(queue):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for index, row in enumerate(reader):
                book_id = row['Book Id']
                title = row['Title']
                author = row['Author']
                author_lf = row['Author l-f']
                additional_authors = row['Additional Authors']
                isbn = row['ISBN'].replace('="', '').replace('"', '')
                isbn13 = row['ISBN13'].replace('="', '').replace('"', '')
                my_rating = row['My Rating']
                average_rating = row['Average Rating']
                publisher = row['Publisher']
                binding = row['Binding']
                number_of_pages = row['Number of Pages']
                year_published = row['Year Published']
                original_publication_year = row['Original Publication Year']
                date_read = row['Date Read']
                date_added = row['Date Added']
                bookshelves = row['Bookshelves']
                bookshelves_with_positions = row['Bookshelves with positions']
                exclusive_shelf = row['Exclusive Shelf']
                my_review = row['My Review']
                spoiler = row['Spoiler']
                private_notes = row['Private Notes']
                read_count = row['Read Count']
                owned_copies = row['Owned Copies']
                
                if not isbn or isbn == "":
                    logging.warning(f"No valid ISBN for {title}, attempting to find ISBN.")
                    isbn = find_isbn(title, author)
                
                cover_image = find_cover_image(isbn, isbn13, title, author)
                
                # Check for duplicates
                if any(book['title'] == title and book['author'] == author for book in books):
                    logging.warning(f"Duplicate entry found for {title} by {author}. Skipping.")
                    continue
                
                books.append({
                    "user_id": user_id,  # Include user_id
                    "book_id": book_id,
                    "title": title,
                    "author": author,
                    "author_lf": author_lf,
                    "additional_authors": additional_authors,
                    "isbn": isbn,
                    "isbn13": isbn13,
                    "my_rating": my_rating,
                    "average_rating": average_rating,
                    "publisher": publisher,
                    "binding": binding,
                    "number_of_pages": number_of_pages,
                    "year_published": year_published,
                    "original_publication_year": original_publication_year,
                    "date_read": date_read,
                    "date_added": date_added,
                    "bookshelves": bookshelves,
                    "bookshelves_with_positions": bookshelves_with_positions,
                    "exclusive_shelf": exclusive_shelf,
                    "my_review": my_review,
                    "spoiler": spoiler,
                    "private_notes": private_notes,
                    "read_count": read_count,
                    "owned_copies": owned_copies,
                    "cover": cover_image
                })
                
                # Update progress bar
                progress_bar['value'] = index + 1
                progress_window.update_idletasks()
        
        queue.put(books)
    
    def save_books_from_queue(queue):
        books = queue.get()
        db.save_books(books)
        middle_pane.render_bookshelf(books)
        progress_window.destroy()
    
    queue = Queue()
    threading.Thread(target=process_csv, args=(queue,)).start()
    root.after(100, check_queue, root, queue, save_books_from_queue)

def check_queue(root, queue, callback):
    if not queue.empty():
        callback(queue)
    else:
        root.after(100, check_queue, root, queue, callback)
