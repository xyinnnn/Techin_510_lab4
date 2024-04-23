# db.py
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        load_dotenv()  # Load environment variables
        self.connection = psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        if self.cursor is not None:
            self.cursor.close()
    
    def create_books_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                price NUMERIC(5,2),
                rating VARCHAR(10),
                stock VARCHAR(50)
            );
        """)
        self.connection.commit()

    def insert_book(self, title, price, rating, stock):
        self.cursor.execute("""
            INSERT INTO books (title, price, rating, stock) 
            VALUES (%s, %s, %s, %s);
        """, (title, price, rating, stock))
        self.connection.commit()
