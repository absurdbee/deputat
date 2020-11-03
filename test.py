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

def get_links(url):
    soup = BeautifulSoup(url, 'lxml')
    list = []
    container = soup.find('div', class_='content__in content__in_bottom')
    blocks = container.find_all('a', class_='group__persons__item group__persons__item_with_photo')
    for item in blocks:
        list += [1,]
    return blocks

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_='article__title--person')
    if not name:
        name = soup.find('h2', class_='person__title person__title--l')
    _name = str(name)
    person__description = soup.find('div', class_='person__description__grid')
    fraction = person__description.find('a', class_='person__description__link').text

    description = soup.find('div', class_='article__lead article__lead--person')
    if not description:
        description = soup.find('div', class_='page__lead')
    description = description.text
    image = soup.find('img', class_='person__image person__image--mobile')
    if not image:
        image = soup.find('img', class_='person__image person__image--l')
    #save_image(get_name(image['src']), get_file(image['src']))

    content__s = soup.find('div', class_='content--s')
    birthday = content__s.find_all('p')[0].text
    authorization = content__s.find_all('p')[1].text

    definitions_list_1 = soup.find_all('dl', class_='definitions-list')[0]
    dd_1 = definitions_list_1.find('dd')
    election_information = dd_1.find_all('p')[0].text + definitions_list_1.find('dt').text

    definitions_list_2 = soup.find('dl', class_='definitions-list definitions-list--capitalize')
    edu_count = 0
    edu_list = []
    edu_dd = definitions_list_2.find_all('dd')
    edu_dt = definitions_list_2.find_all('dt')
    for dd in edu_dd:
        dd__dt = edu_dd[edu_count].text + ": " + edu_dt[edu_count].text
        edu_list += [dd__dt, ]
        edu_count += 1

    list = AuthorityList.objects.get(slug="state_duma")
    region_list = soup.find_all('div', class_='person__description__col')[3].text

    data = {'name': _name.replace('<h1 class="article__title article__title--person">', '').replace('<br/>', ' ').replace('</h1>', ''),
            'fraction': fraction,
            'image': 'http://duma.gov.ru' + image['src'],
            'description': description,
            'list': list,
            'educations_list': edu_list,
            'region_list': region_list.replace(", ", ",").split(","),
            'birthday': birthday.replace('Дата рождения: ', ''),
            'election_information': election_information.replace('\n', '').strip().replace('                   ', ':'),
            'authorization': authorization.replace('\n', '').strip().replace('Дата вступления в полномочия:                                 ', '')}
    return data


def main():
    html = get_html("http://council.gov.ru/structure/members/")
    lists = get_links(html)
    print(lists)

if __name__ == '__main__':
    main()
