import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com/page/{page}/'


page = 1
while True:
    url = BASE_URL.format(page=page)
    print(f"Scraping {url}")
    response = requests.get(url)

    if 'No quotes found' in response.text:
        break
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_divs = soup.select('div.quote')

quotes = []
for quote_div in quote_divs:
    quote = {}
    quote['content'] = quote_div.select_one('span.text').text
    quote['author'] = quote_div.select_one('small.author').text
    quote['author_link'] = quote_div.select_one('span')[1].select('a')[0]
    quote['tags'] = [tag.text for tag in quote_div.select('a.tag')]
    quote['tag_links'] = [tag['herf'] for tag in quote_div.select('a.tag')]
    quotes.append(quote)
page += 1

print(quotes)

