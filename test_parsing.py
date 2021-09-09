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
from okrug.models import Okrug


def get_html(url):
    r = requests.get(url)
    return r.text

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    h5_list = soup.find_all('h5')
    h5_count = 0

    tgrids = soup.find_all('div', class_='tgrid')
    parth = 0
    for tgrid in tgrids:
        h5_count = h5_count + 2

        deputat_items = tgrid.find_all('div', class_='trow')
        count = 0
        parth += 1

        for item in deputat_items:
            if not count == 0:

                name = item.find("b").text
                deps = item.find_all('li')

                print(name)
                print(item.find("p", class_='fio').text.replace(name + ", ",""))
                if "Возраст" in deps[0].text:
                    print(deps[0].text.replace("Возраст: ",""))
                else:
                    print(deps[1].text.replace("Возраст: ",""))
                print(deps[2].text.replace("Образование: ",""))
            count += 1
            print("--------------------")
        print("=======================")

def main():
    html = get_html("https://gosduma-2021.com/s/altaiskii-krai/")
    get_page_data(html)

if __name__ == '__main__':
    main()
