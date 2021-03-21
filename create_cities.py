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
    return r.text

def main():
    html = get_html("https://hramy.ru/regions/city_reg.htm")
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('div', class_='contpost')
    list = body.find_all('tr')
    #next(list)

    for item in list:
        for cell in item.find_all('td'):
            print(cell.text)

if __name__ == '__main__':
    main()
