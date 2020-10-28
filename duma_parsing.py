import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = text_before_word(soup.find('div', class_='article__title article__title--person').text)
    except:
        name = ''
    try:
        fraction = text_before_word(soup.find('div', class_='link link--underline person__description__link').text)
    except:
        fraction = ''
    data = {'name': name,
            'fraction': fraction}
    return data


def main():
    start = datetime.now()
    url = 'http://duma.gov.ru/duma/persons/99112808/'
    html = get_html(url)
    data = get_page_data(html)
    #return data 

if __name__ == '__main__':
    main()
