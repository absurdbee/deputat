# -*- coding: utf-8 -*-
from locale import *
import sys,os
import re
import requests
from bs4 import BeautifulSoup

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from lists.models import AuthorityList


def get_html(url):
    r = requests.get(url)
    return r.text

def get_file(url):
    r = requests.get(url, stream=True)
    return r

def get_name(url):
    name = url.split('/')[-1]
    return name

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_='article__title--person')
    #_name = str(name)
    fraction = soup.find('a', class_='person__description__link').text
    description = soup.find('div', class_='article__lead article__lead--person').text
    image = soup.find('img', class_='person__image person__image--mobile')

    content__s = soup.find('div', class_='content--s')
    birthday = content__s.find_all('p')[0].text
    authorization = content__s.find_all('p')[1].text

    list = AuthorityList.objects.get(slug="state_duma")
    region_list = soup.find('div', class_='person__description__col').text

    data = {#'name': name.replace('<h1 class="article__title article__title--person">', '').replace('<br/>', ' ').replace('</h1>', ''),
            'name': name,
            'fraction': fraction,
            'image': 'http://duma.gov.ru' + image['src'],
            'description': description,
            'list': list,
            'region_list': region_list,
            'birthday': birthday,
            'authorization': authorization}
    return data


def main():
    url = 'http://duma.gov.ru/duma/persons/99112789/'
    html = get_html(url)
    data = get_page_data(html)
    print(data)

if __name__ == '__main__':
    main()
