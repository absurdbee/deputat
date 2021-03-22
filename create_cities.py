import sys,os
import re
import requests
from bs4 import BeautifulSoup

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from lists.models import *
from elect.models import *

def get_html(url):
    r = requests.get(url)
    return r.text.encode().decode('latin1')

def main():
    html = get_html("https://hramy.ru/regions/city_reg.htm")
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('div', class_='contpost')
    list = body.find_all('tr')
    for item in list:
        i = 0
        for cell in item.find_all('td'):
            i += 1
            if i == 1:
                print("a" + cell.text)
            elif i == 4:
                print("b" + cell.text)

if __name__ == '__main__':
    main()
