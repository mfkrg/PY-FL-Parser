import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.fl.ru/projects/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0', 'accept': '*/*'}
HOST = 'https://www.fl.ru'
FILE = 'offers.csv'

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
    return offers

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        offers = []
        pages_count = get_pages_count(html.text)
        for page in range(1, 20):
            print(f'Пытаюсь найти что-то годное! Страница {page} из 19...')
            html = get_html(URL, params={'page': page})
            offers.extend(get_content(html.text))
        save_file(offers, FILE)
        print(f'Пропарсили {len(offers)} предложений')
    else:
        print("Error")

parse()