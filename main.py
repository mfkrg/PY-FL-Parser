import requests
from bs4 import BeautifulSoup

URL = 'https://www.fl.ru/projects/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0', 'accept': '*/*'}
HOST = 'https://www.fl.ru'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.findAll('li', class_='b-pager__item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('h2', class_='b-post__title')

    offers = []

    for item in items:
        offers.append({
            'title': item.find('a', class_='b-post__link').get_text(strip=True),
            'link': HOST + item.find('a', class_='b-post__link').get('href')
        })
    print(offers)


def parse():
    html = get_html(URL)
    if (html.status_code == 200):
        #offers = get_content(html.text)
        pages_count = get_pages_count(html.text)
        print(pages_count)
    else:
        print("Error")

parse()