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
                if item.find_all('td')[3].text == "Красноярский Край":
                    region = Region.objects.get(name="Красноярский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Приморский Край":
                    region = Region.objects.get(name="Приморский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Ставропольский Край":
                    region = Region.objects.get(name="Ставропольский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Хабаровский Край":
                    region = Region.objects.get(name="Хабаровский край")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Амурская Область":
                    region = Region.objects.get(name="Амурская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Архангельская Область":
                    region = Region.objects.get(name="Архангельская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Астраханская Область":
                    region = Region.objects.get(name="Астраханская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Белгородская Область":
                    region = Region.objects.get(name="Белгородская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")
                elif item.find_all('td')[3].text == "Брянская Область":
                    region = Region.objects.get(name="Брянская область")
                    City.objects.create(name=item.find_all('td')[0].text, region=region)
                    print("гогод " + item.find_all('td')[0].text + " Добавлен!")

if __name__ == '__main__':
    main()
