import requests
from bs4 import BeautifulSoup
from db import Database  # Import the Database class from db.py

BASE_URL = "http://books.toscrape.com/"

def scrape_books():
    with Database() as db:
        db.create_books_table()  # Ensure the table is prepared

        page = 1
        while True:
            url = BASE_URL.format(page=page)
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

if __name__ == "__main__":
    scrape_books()

