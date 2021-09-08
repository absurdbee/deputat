import sys,os
import re
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from district.models import District2
from lists.models import Fraction, AuthorityList
from elect.models import Elect


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html, district):
    soup = BeautifulSoup(html, 'lxml')

    tgrids = soup.find_all('div', class_='tgrid')
    deputat_items = tgrids[0].find_all('div', class_='trow')
    count = 0

    for item in deputat_items:
        if count == 0:
            pass
        print("фИО ", item.find("b").text)
        print("Фото ", "https://gosduma-2021.com/" + item.find("img")["src"])
        print("Партия ", item.find('p', class_='party-name').text)

        deps = item.find_all('ul', class_='listdep')

        print("Должность ", item.find("p", class_='fio').text)
        print("Возраст ", deps[1].text)
        print("Образование ", deps[2].text))
        count += 1
        print("=================================")

def main():
    html = get_html("https://gosduma-2021.com/s/volgogradskaya-oblast/")
    get_page_data(html)

if __name__ == '__main__':
    main()
