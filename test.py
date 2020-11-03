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

test_id = ['http://council.gov.ru/structure/persons/1317/', ]

def get_html(url):
    r = requests.get(url)
    return r.text

def get_links(url):
    soup = BeautifulSoup(url, 'lxml')
    list = []
    container = soup.find('div', class_='main__content_wrapper')
    blocks = container.find_all('a', class_='group__persons__item group__persons__item_with_photo')
    for item in blocks:
        list += ['http://council.gov.ru' + item['href'], ]
    return list

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    name = soup.find('h2', class_='senators_title')

    person__description = soup.find('div', class_='person__description__grid')

    description = soup.find('div', class_='person__additional_top').text

    img_container = soup.find('div', class_='content__in')
    image = img_container.find('img', class_='person_img')

    person_info = soup.find('div', class_='person_info_private')
    birthday = person_info.find_all('p')[0].text
    authorization = person_info_.find_all('p')[1].text
    term_of_office = person_info_.find_all('p')[1].text

    person_biography = soup.find('div', class_='person__biography')
    edu_container = person_biography.find_all('div', class_='biography_block')[0]
    edu_p = person_biography.find_all('p')
    edu_count = 0
    edu_list = []
    for p in edu_p:
        edu_item = edu_p[edu_count].text
        edu_list += [edu_item, ]
        edu_count += 1
    region = soup.find_all('a', class_='region_name_link').text

    data = {'name': name.text,
            'image': 'http://council.gov.ru' + image['src'],
            'description': description,
            'educations_list': edu_list,
            'region': region,
            'birthday': birthday.replace('Дата рождения: ', ''),
            'authorization': authorization.replace('\n', '').strip().replace('Дата наделения полномочиями: ', ''),
            'term_of_office': term_of_office.replace('\n', '').strip(),}
    return data


def main():
    html = get_html("http://council.gov.ru/structure/members/")
    lists = get_links(html)
    for url in test_id:
        _html = get_html(url)
        data = get_page_data(_html)
        print(data)

if __name__ == '__main__':
    main()
