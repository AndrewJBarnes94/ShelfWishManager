import sqlite3
import bcrypt
import secrets
import datetime

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
                book_id TEXT,
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT,
                temp_token TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_resets (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                token TEXT,
                expires_at DATETIME,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()
    
    def save_books(self, books):
        """Save books to the SQLite database."""
        for book in books:
            self.cursor.execute("""
                INSERT OR REPLACE INTO books (
                    id, book_id, title, author, author_lf, additional_authors, isbn, isbn13, my_rating, average_rating,
                    publisher, binding, number_of_pages, year_published, original_publication_year, date_read, date_added,
                    bookshelves, bookshelves_with_positions, exclusive_shelf, my_review, spoiler, private_notes, read_count,
                    owned_copies, cover
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                book.get("id"), book["book_id"], book["title"], book["author"], book["author_lf"], book["additional_authors"], book["isbn"], book["isbn13"], book["my_rating"], book["average_rating"], book["publisher"], book["binding"], book["number_of_pages"], book["year_published"], book["original_publication_year"], book["date_read"], book["date_added"], book["bookshelves"], book["bookshelves_with_positions"], book["exclusive_shelf"], book["my_review"], book["spoiler"], book["private_notes"], book["read_count"], book["owned_copies"], book["cover"]
            ))
        self.conn.commit()
    
    def load_books(self):
        """Load books from the SQLite database."""
        self.cursor.execute("SELECT id, book_id, title, author, author_lf, additional_authors, isbn, isbn13, my_rating, average_rating, publisher, binding, number_of_pages, year_published, original_publication_year, date_read, date_added, bookshelves, bookshelves_with_positions, exclusive_shelf, my_review, spoiler, private_notes, read_count, owned_copies, cover FROM books")
        rows = self.cursor.fetchall()
        return [{"id": row[0], "book_id": row[1], "title": row[2], "author": row[3], "author_lf": row[4], "additional_authors": row[5], "isbn": row[6], "isbn13": row[7], "my_rating": row[8], "average_rating": row[9], "publisher": row[10], "binding": row[11], "number_of_pages": row[12], "year_published": row[13], "original_publication_year": row[14], "date_read": row[15], "date_added": row[16], "bookshelves": row[17], "bookshelves_with_positions": row[18], "exclusive_shelf": row[19], "my_review": row[20], "spoiler": row[21], "private_notes": row[22], "read_count": row[23], "owned_copies": row[24], "cover": row[25]} for row in rows]
    
    def get_current_book(self):
        """Get the current book being read from the database."""
        self.cursor.execute("SELECT id, book_id, title, author, author_lf, additional_authors, isbn, isbn13, my_rating, average_rating, publisher, binding, number_of_pages, year_published, original_publication_year, date_read, date_added, bookshelves, bookshelves_with_positions, exclusive_shelf, my_review, spoiler, private_notes, read_count, owned_copies, cover FROM books WHERE exclusive_shelf = 'currently-reading'")
        row = self.cursor.fetchone()
        if row:
            return {"id": row[0], "book_id": row[1], "title": row[2], "author": row[3], "author_lf": row[4], "additional_authors": row[5], "isbn": row[6], "isbn13": row[7], "my_rating": row[8], "average_rating": row[9], "publisher": row[10], "binding": row[11], "number_of_pages": row[12], "year_published": row[13], "original_publication_year": row[14], "date_read": row[15], "date_added": row[16], "bookshelves": row[17], "bookshelves_with_positions": row[18], "exclusive_shelf": row[19], "my_review": row[20], "spoiler": row[21], "private_notes": row[22], "read_count": row[23], "owned_copies": row[24], "cover": row[25]}
        return None
    
    def delete_book(self, id):
        """Delete a book from the SQLite database by its ID."""
        self.cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        self.conn.commit()
    
    def create_user(self, username, email, password):
        """Create a new user with a hashed password."""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
        self.conn.commit()
    
    def authenticate_user(self, username, password):
        """Authenticate a user by checking the hashed password or temporary token."""
        self.cursor.execute("SELECT id, password_hash, temp_token FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            user_id, password_hash, temp_token = row
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                return user_id, False  # Regular login
            elif temp_token and temp_token == password:
                self.cursor.execute("UPDATE users SET temp_token = NULL WHERE id = ?", (user_id,))
                self.conn.commit()
                return user_id, True  # Temporary token login
        return None, False
    
    def get_user_by_email(self, email):
        """Get a user by their email address."""
        self.cursor.execute("SELECT id, username FROM users WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        return {"id": row[0], "username": row[1]} if row else None
    
    def create_password_reset_token(self, user_id):
        """Create a password reset token for a user."""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        self.cursor.execute("INSERT INTO password_resets (user_id, token, expires_at) VALUES (?, ?, ?)", (user_id, token, expires_at))
        self.conn.commit()
        return token
    
    def verify_password_reset_token(self, token):
        """Verify a password reset token."""
        self.cursor.execute("SELECT user_id FROM password_resets WHERE token = ? AND expires_at > ?", (token, datetime.datetime.now()))
        row = self.cursor.fetchone()
        return row[0] if row else None
    
    def reset_password(self, user_id, new_password):
        """Reset a user's password."""
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        self.cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
        self.conn.commit()
        self.cursor.execute("DELETE FROM password_resets WHERE user_id = ?", (user_id,))
        self.conn.commit()
    
    def create_temp_token(self, user_id):
        """Create a temporary token for one-time login."""
        temp_token = secrets.token_urlsafe(16)
        self.cursor.execute("UPDATE users SET temp_token = ? WHERE id = ?", (temp_token, user_id))
        self.conn.commit()
        return temp_token
