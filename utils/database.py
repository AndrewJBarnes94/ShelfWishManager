import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("books.db")
        self.cursor = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        """Initialize the SQLite database."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                title TEXT,
                author TEXT,
                author_lf TEXT,
                additional_authors TEXT,
                isbn TEXT,
                isbn13 TEXT,
                my_rating INTEGER,
                average_rating REAL,
                publisher TEXT,
                binding TEXT,
                number_of_pages INTEGER,
                year_published INTEGER,
                original_publication_year INTEGER,
                date_read TEXT,
                date_added TEXT,
                bookshelves TEXT,
                bookshelves_with_positions TEXT,
                exclusive_shelf TEXT,
                my_review TEXT,
                spoiler TEXT,
                private_notes TEXT,
                read_count INTEGER,
                owned_copies INTEGER,
                cover BLOB
            )
        """)
        self.conn.commit()
    
    def save_books(self, books):
        """Save books to the SQLite database."""
        self.cursor.execute("DELETE FROM books")
        for book in books:
            self.cursor.execute("""
                INSERT INTO books (
                    book_id, title, author, author_lf, additional_authors, isbn, isbn13, my_rating, average_rating,
                    publisher, binding, number_of_pages, year_published, original_publication_year, date_read, date_added,
                    bookshelves, bookshelves_with_positions, exclusive_shelf, my_review, spoiler, private_notes, read_count,
                    owned_copies, cover
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book["book_id"], book["title"], book["author"], book["author_lf"], book["additional_authors"], book["isbn"], book["isbn13"], book["my_rating"], book["average_rating"], book["publisher"], book["binding"], book["number_of_pages"], book["year_published"], book["original_publication_year"], book["date_read"], book["date_added"], book["bookshelves"], book["bookshelves_with_positions"], book["exclusive_shelf"], book["my_review"], book["spoiler"], book["private_notes"], book["read_count"], book["owned_copies"], book["cover"]
            ))
        self.conn.commit()
    
    def load_books(self):
        """Load books from the SQLite database."""
        self.cursor.execute("SELECT book_id, title, author, author_lf, additional_authors, isbn, isbn13, my_rating, average_rating, publisher, binding, number_of_pages, year_published, original_publication_year, date_read, date_added, bookshelves, bookshelves_with_positions, exclusive_shelf, my_review, spoiler, private_notes, read_count, owned_copies, cover FROM books")
        rows = self.cursor.fetchall()
        return [{"book_id": row[0], "title": row[1], "author": row[2], "author_lf": row[3], "additional_authors": row[4], "isbn": row[5], "isbn13": row[6], "my_rating": row[7], "average_rating": row[8], "publisher": row[9], "binding": row[10], "number_of_pages": row[11], "year_published": row[12], "original_publication_year": row[13], "date_read": row[14], "date_added": row[15], "bookshelves": row[16], "bookshelves_with_positions": row[17], "exclusive_shelf": row[18], "my_review": row[19], "spoiler": row[20], "private_notes": row[21], "read_count": row[22], "owned_copies": row[23], "cover": row[24]} for row in rows]
    
    def get_current_book(self):
        """Get the current book being read from the database."""
        self.cursor.execute("SELECT book_id, title, author, author_lf, additional_authors, isbn, isbn13, my_rating, average_rating, publisher, binding, number_of_pages, year_published, original_publication_year, date_read, date_added, bookshelves, bookshelves_with_positions, exclusive_shelf, my_review, spoiler, private_notes, read_count, owned_copies, cover FROM books WHERE exclusive_shelf = 'currently-reading'")
        row = self.cursor.fetchone()
        if row:
            return {"book_id": row[0], "title": row[1], "author": row[2], "author_lf": row[3], "additional_authors": row[4], "isbn": row[5], "isbn13": row[6], "my_rating": row[7], "average_rating": row[8], "publisher": row[9], "binding": row[10], "number_of_pages": row[11], "year_published": row[12], "original_publication_year": row[13], "date_read": row[14], "date_added": row[15], "bookshelves": row[16], "bookshelves_with_positions": row[17], "exclusive_shelf": row[18], "my_review": row[19], "spoiler": row[20], "private_notes": row[21], "read_count": row[22], "owned_copies": row[23], "cover": row[24]}
        return None
