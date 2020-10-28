import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_='article__title article__title--person').text.strip()
    except:
        name = ''
    try:
        fraction = soup.find('a', class_='person__description__link').text.strip()
    except:
        fraction = ''
    data = {'name': name,
            'fraction': fraction}
    return data


def main():
    url = 'http://duma.gov.ru/duma/persons/99112808/'
    html = get_html(url)
    data = get_page_data(html)
    print(data)

if __name__ == '__main__':
    main()
