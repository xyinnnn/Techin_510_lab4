import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from db import Database  # Ensure this import statement is correct based on your project structure

BASE_URL = "http://books.toscrape.com/"

def scrape_books():
    with Database() as db:
        db.create_books_table()  # Ensure the table is prepared

        page = 1
        while True:
            url = f"{BASE_URL}catalogue/page-{page}.html"  # Use f-string for cleaner formatting
            response = requests.get(url)
            if response.status_code != 200:
                break  # Stop if URL is not accessible or finished

            soup = BeautifulSoup(response.content, 'html.parser')
            books = soup.find_all('article', class_='product_pod')
            if not books:
                break  # Stop if no books found on page

            for book in books:
                title = book.find('h3').a['title']
                price = book.find('p', class_='price_color').text.lstrip('£')
                rating = book.find('p', class_='star-rating').get('class')[1]
                stock = book.find('p', class_='instock availability').text.strip()

                db.insert_book(title, float(price), rating, stock)

            page += 1

def fetch_books(search_query="", filter_rating=None, filter_price=None):
    with Database() as db:
        # Construct the query
        query = """
            SELECT id AS ID, title AS Title, price AS Price, rating AS Rating, stock AS Stock FROM books
        """
        conditions = []
        params = []
        
        if search_query:
            conditions.append("title LIKE %s")
            params.append('%' + search_query + '%')
        if filter_rating:
            conditions.append("rating = %s")
            params.append(filter_rating)
        if filter_price is not None:
            conditions.append("price <= %s")
            params.append(filter_price)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        db.cursor.execute(query, params)
        rows = db.cursor.fetchall()
        df = pd.DataFrame(rows, columns=['id', 'title', 'price', 'rating', 'stock'])
        return df

# Streamlit UI Components
st.title('Book Finder')

if st.button('Scrape Books First'):
    scrape_books()
    st.success('Books were scraped successfully.')

search_query = st.text_input('Search for books by title')
filter_rating = st.selectbox('Rating', ('', 'One', 'Two', 'Three', 'Four', 'Five'))
filter_price = st.slider('Max Price', 0, 100, 50)

if st.button('Search'):
    results = fetch_books(search_query, filter_rating, filter_price)
else:
    results = fetch_books()

if results.empty:
    st.write("No books found.")
else:
    st.write("Books found:", results.shape[0])
    st.dataframe(results)

    for index, book in results.iterrows():
        with st.expander(f"{book['title']} - £{book['price']}"):
            st.write(f"Rating: {book['rating']}")
            st.write(f"Stock: {book['stock']}")
