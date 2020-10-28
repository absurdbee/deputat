# -*- coding: utf-8 -*-
#from locale import *
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
    if not name:
        name = soup.find('h2', class_='person__title person__title--l')
    _name = str(name)
    fraction = soup.find('a', class_='person__description__link').text
    description = soup.find('div', class_='article__lead article__lead--person')
    if not description:
        description = soup.find('div', class_='page__lead')
    description = description.text
    image = soup.find('img', class_='person__image person__image--mobile')

    content__s = soup.find('div', class_='content--s')
    birthday = content__s.find_all('p')[0].text
    authorization = content__s.find_all('p')[1].text

    definitions_list_1 = soup.find_all('dl', class_='definitions-list')[0]
    dd = definitions_list_1.find('dd')
    election_information = dd.find_all('p')[0].text + definitions_list_1.find('dt').text

    list = AuthorityList.objects.get(slug="state_duma")
    region_list = soup.find_all('div', class_='person__description__col')[3].text

    data = {'name': _name.replace('<h1 class="article__title article__title--person">', '').replace('<br/>', ' ').replace('</h1>', ''),
            'fraction': fraction,
            'image': 'http://duma.gov.ru' + image['src'],
            'description': description,
            'list': list,
            'region_list': region_list,
            'birthday': birthday.replace('Дата рождения: ', ''),
            'election_information': election_information.replace('\n', '').strip().replace('                   ', ':'),
            'authorization': authorization.replace('\n', '').strip().replace('Дата вступления в полномочия:                                 ', '')}
    return data


def main():
    url = 'http://duma.gov.ru/duma/persons/99100829/'
    html = get_html(url)
    data = get_page_data(html)
    print(data)

if __name__ == '__main__':
    main()
