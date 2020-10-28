import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_='article__title article__title--person')
    _name = str(name)

    try:
        fraction = soup.find('a', class_='person__description__link').text
    except:
        fraction = ''
    data = {'name': _name.replace('<h1 class="article__title article__title--person">', '').replace('<br/>', ' ').replace('<h1/>', ''),
            'fraction': fraction}
    return data


def main():
    url = 'http://duma.gov.ru/duma/persons/99112808/'
    html = get_html(url)
    data = get_page_data(html)
    print(data)

if __name__ == '__main__':
    main()
