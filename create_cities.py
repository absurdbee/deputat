https://telegram.me/share/url?url=<get_absolute_url>&text=<title>

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

from city.models import City
from region.models import Region

def get_html(url):
    headers = {"User-Agent": USERAGENT}
    resp = requests.get(url, headers=headers)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    return resp.text

def main():
    resp = requests.get("https://hramy.ru/regions/city_reg.htm")
    soup = BeautifulSoup(resp.content, 'lxml')
    body = soup.find('div', class_='contpost')
    list = body.find_all('tr')
    p = 0
    for item in list:
        p += 1
        if p != 1:
            if City.objects.filter(name=item.find_all('td')[0].text).exists():
                print("гогод " + item.find_all('td')[0].text + " уже сохранён...")
            else:
                if item.find_all('td')[3].text == "Чукотский Автономный округ":
                    region = Region.objects.get(name="Чукотский автономный округ")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ямало-Ненецкий Автономный округ":
                    region = Region.objects.get(name="Ямало-Ненецкий автономный округ")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Крым Республика":
                    region = Region.objects.get(name="Республика Крым")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Севастополь Город":
                    region = Region.objects.get(name="Севастополь")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ярославская Область":
                    region = Region.objects.get(name="Ярославская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Москва Город":
                    region = Region.objects.get(name="Москва")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Санкт-Петербург Город":
                    region = Region.objects.get(name="Санкт-Петербург")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Еврейская Автономная область":
                    region = Region.objects.get(name="Еврейская автономная область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ненецкий Автономный округ":
                    region = Region.objects.get(name="Ненецкий автономный округ")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ханты-Мансийский Автономный округ - Югра Автономный округ":
                    region = Region.objects.get(name="Ханты-Мансийский автономный округ - Югра (Тюменская область)")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Адыгея Республика":
                    region = Region.objects.get(name="Республика Адыгея")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Башкортостан Республика":
                    region = Region.objects.get(name="Республика Башкортостан")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Бурятия Республика":
                    region = Region.objects.get(name="Республика Бурятия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Алтай Республика":
                    region = Region.objects.get(name="Алтайский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Дагестан Республика":
                    region = Region.objects.get(name="Республика Дагестан")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ингушетия Республика":
                    region = Region.objects.get(name="Республика Ингушетия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Кабардино-Балкарская Республика":
                    region = Region.objects.get(name="Кабардино-Балкарская Республика")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Калмыкия Республика":
                    region = Region.objects.get(name="Республика Калмыкия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Карачаево-Черкесская Республика":
                    region = Region.objects.get(name="Карачаево-Черкесская Республика")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Карелия Республика":
                    region = Region.objects.get(name="Республика Карелия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Коми Республика":
                    region = Region.objects.get(name="Республика Коми")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Марий Эл Республика":
                    region = Region.objects.get(name="Республика Марий Эл")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Мордовия Республика":
                    region = Region.objects.get(name="Республика Мордовия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Саха /Якутия/ Республика":
                    region = Region.objects.get(name="Республика Саха (Якутия)")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Северная Осетия - Алания Республика":
                    region = Region.objects.get(name="Республика Северная Осетия - Алания")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Москва Город":
                    region = Region.objects.get(name="Москва")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Татарстан Республика":
                    region = Region.objects.get(name="Республика Татарстан")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Тыва Республика":
                    region = Region.objects.get(name="Республика Тыва")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Удмуртская Республика":
                    region = Region.objects.get(name="Удмуртская Республика (Удмуртия)")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Хакасия Республика":
                    region = Region.objects.get(name="Республика Хакасия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Чеченская Республика":
                    region = Region.objects.get(name="Чеченская Республика")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Чувашская Республика - Чувашия":
                    region = Region.objects.get(name="Чувашская Республика - Чувашия")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Алтайский Край":
                    region = Region.objects.get(name="Алтайский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Краснодарский Край":
                    region = Region.objects.get(name="Краснодарский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Красноярский Край":
                    region = Region.objects.get(name="Красноярский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Приморский Край":
                    region = Region.objects.get(name="Приморский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ставропольский Край":
                    region = Region.objects.get(name="Ставропольский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Хабаровский Край":
                    region = Region.objects.get(name="Хабаровский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Амурская Область":
                    region = Region.objects.get(name="Амурская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Архангельская Область":
                    region = Region.objects.get(name="Архангельская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")

                elif item.find_all('td')[3].text == "Белгородская Область":
                    region = Region.objects.get(name="Белгородская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Брянская Область":
                    region = Region.objects.get(name="Брянская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Владимирская Область":
                    region = Region.objects.get(name="Владимирская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Волгоградская Область":
                    region = Region.objects.get(name="Волгоградская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Вологодская Область":
                    region = Region.objects.get(name="Вологодская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Воронежская Область":
                    region = Region.objects.get(name="Воронежская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ивановская Область":
                    region = Region.objects.get(name="Ивановская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Иркутская Область":
                    region = Region.objects.get(name="Иркутская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Калининградская Область":
                    region = Region.objects.get(name="Калининградская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Калужская Область":
                    region = Region.objects.get(name="Калужская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Камчатский Край":
                    region = Region.objects.get(name="Камчатский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Кемеровская Область":
                    region = Region.objects.get(name="Кемеровская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Кировская Область":
                    region = Region.objects.get(name="Кировская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Костромская Область":
                    region = Region.objects.get(name="Костромская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Курганская Область":
                    region = Region.objects.get(name="Курганская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Курская Область":
                    region = Region.objects.get(name="Курская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ленинградская Область":
                    region = Region.objects.get(name="Ленинградская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Липецкая Область":
                    region = Region.objects.get(name="Липецкая область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Магаданская Область":
                    region = Region.objects.get(name="Магаданская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Московская Область":
                    region = Region.objects.get(name="Московская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Мурманская Область":
                    region = Region.objects.get(name="Мурманская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Нижегородская Область":
                    region = Region.objects.get(name="Нижегородская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Новгородская Область":
                    region = Region.objects.get(name="Новгородская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Новосибирская Область":
                    region = Region.objects.get(name="Новосибирская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Омская Область":
                    region = Region.objects.get(name="Омская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Оренбургская Область":
                    region = Region.objects.get(name="Оренбургская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Орловская Область":
                    region = Region.objects.get(name="Орловская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Пензенская Область":
                    region = Region.objects.get(name="Пензенская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Пермский Край":
                    region = Region.objects.get(name="Пермский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Псковская Область":
                    region = Region.objects.get(name="Псковская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ростовская Область":
                    region = Region.objects.get(name="Ростовская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Рязанская Область":
                    region = Region.objects.get(name="Рязанская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Самарская Область":
                    region = Region.objects.get(name="Самарская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Саратовская Область":
                    region = Region.objects.get(name="Саратовская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Сахалинская Область":
                    region = Region.objects.get(name="Сахалинская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Свердловская Область":
                    region = Region.objects.get(name="Свердловская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Смоленская Область":
                    region = Region.objects.get(name="Смоленская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Тамбовская Область":
                    region = Region.objects.get(name="Тамбовская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Тверская Область":
                    region = Region.objects.get(name="Тверская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Томская Область":
                    region = Region.objects.get(name="Томская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")

                elif item.find_all('td')[3].text == "Тульская Область":
                    region = Region.objects.get(name="Тульская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Тюменская Область":
                    region = Region.objects.get(name="Тюменская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ульяновская Область":
                    region = Region.objects.get(name="Ульяновская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Челябинская Область":
                    region = Region.objects.get(name="Челябинская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Забайкальский Край":
                    region = Region.objects.get(name="Забайкальский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ярославская Область":
                    region = Region.objects.get(name="Ярославская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("город " + item.find_all('td')[0].text + " Добавлен!")

if __name__ == '__main__':
    main()
