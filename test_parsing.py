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

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    h5_list = soup.find_all('h5')
    h5_count = 0

    tgrids = soup.find_all('div', class_='tgrid')
    parth = 0
    for tgrid in tgrids:
        print(h5_list[h5_count].text)
        h5_count = h5_count + 2

        deputat_items = tgrid.find_all('div', class_='trow')
        count = 0
        parth += 1

        for item in deputat_items:
            if not count == 0:
                name = item.find("b").text
                print("фИО ", name)
                #print("Фото ", "https://gosduma-2021.com/" + item.find("img")["src"])
                patr = item.find('p', class_='party-name').text
                if patr == "ЕДИНАЯ РОССИЯ":
                    _patr = Fraction.objects.get(name="Единая Россия")
                elif patr == "ЛДПР":
                    _patr = Fraction.objects.get(name="ЛДПР")
                elif patr == "КПРФ":
                    _patr = Fraction.objects.get(name="КПРФ")
                elif patr == "СПРАВЕДЛИВАЯ РОССИЯ - ЗА ПРАВДУ":
                    _patr = Fraction.objects.get(name="Справедливая Россия")
                else:
                    _patr = Fraction.objects.get(slug="no_fraction")
                print("Партия ", _patr)

                deps = item.find_all('li')

                #print("Должность ", item.find("p", class_='fio').text.replace(name + ", ",""))
                #print("Возраст ", deps[1].text.replace("Возраст: ",""))
                #print("Образование ", deps[2].text.replace("Образование: ",""))
            count += 1
            print("--------------------")
        print("показываю часть ", parth)
        print("=======================")

def main():
    html = get_html("https://gosduma-2021.com/s/evreiskaya-avtonomnaya-oblast/")
    get_page_data(html)

if __name__ == '__main__':
    main()
