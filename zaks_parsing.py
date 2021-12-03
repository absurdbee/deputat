import sys,os
import re
import requests
import time
from bs4 import BeautifulSoup

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from lists.models import *
from elect.models import *

test_id = ['http://council.gov.ru/structure/persons/1317/', ]
sity_names = ['г.Москва', 'г.Санкт-Петербург', 'г.Севастополь', ]

def get_html(url):
    r = requests.get(url)
    return r.text

def get_links(url):
    soup = BeautifulSoup(url, 'lxml')
    list = []
    container = soup.find('div', class_='authors list-materials')
    blocks = container.find_all('div', class_='material')
    for item in blocks:
        list += [item.find('a')['href'],]
    return list

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    block = soup.find('div', class_="tab-content col-xs-8 col-md-9")

    name = soup.find('h2').text

    try:
        image_src = "https://www.assembly.spb.ru/" + block.find('img')['src']
    except:
        image_src = None
    _blocks = block.find_all('p')
    try:
        birthday_block = _blocks[0].text
        _birthday_block = birthday_block.replace("  ", " ")
        __birthday_block = _birthday_block.split(" ")
        birthday = __birthday_block[1] + " " + __birthday_block[2] + " " + __birthday_block[3]
    except:
        birthday_block = _blocks[1].text
        _birthday_block = birthday_block.replace("  ", " ")
        __birthday_block = _birthday_block.split(" ")
        birthday = __birthday_block[1] + " " + __birthday_block[2] + " " + __birthday_block[3]

    data = {'name': name,
            'image': image_src,
            'birthday': birthday.replace('Дата рождения: ', ''),
            }
    return data


def main():
    _list = AuthorityList.objects.get(slug="zaks_2021")
    html = get_html("https://www.assembly.spb.ru/authors/show_convocation/7/")

    soup = BeautifulSoup(html, 'lxml')
    container = soup.find('div', class_='authors list-materials')
    blocks = container.find_all('div', class_='material')

    for item in blocks:
        html = get_html(item.find('a')['href'])
        data = get_page_data(html)

        aaa = item.find_all('a')
        _fraction = aaa[1].text
        if _fraction == 'Фракция "ЕДИНАЯ РОССИЯ"':
            fraction = Fraction.objects.get(slug="edinaya_russia")
        elif _fraction == 'Фракция СПРАВЕДЛИВАЯ РОССИЯ – ПАТРИОТЫ – ЗА ПРАВДУ':
            fraction = Fraction.objects.get(slug="spravedlivaya_russia")
        elif _fraction == 'Фракция КПРФ':
            fraction = Fraction.objects.get(slug="kprf")
        elif _fraction == 'Фракция "ЯБЛОКО"':
            fraction = Fraction.objects.get(slug="yabloko")
        elif _fraction == 'Фракция "Новые люди"':
            fraction = Fraction.objects.get(slug="new_people")
        elif _fraction == 'Фракция ЛДПР':
            fraction = Fraction.objects.get(slug="ldpr")

        if Elect.objects.filter(list=_list, name=data["name"]).exists():
            print("чиновник уже есть - ", data["name"])
        else:
            new_elect = Elect.objects.create(name=data["name"],birthday=data["birthday"],fraction=fraction)
            region = Region.objects.get(name="Санкт-Петербург")
            region.elect_region.add(new_elect)
            if data["image"]:
                new_elect.get_remote_image(data["image"])

            list = AuthorityList.objects.get(slug="senat")
            list.elect_list.add(new_elect)
            print("новый закс - ", data["name"])
        time.sleep(3)

if __name__ == '__main__':
    main()
