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
    image = soup.find('img', class_='person_img')

    person_info = soup.find('div', class_='person_info_private')
    birthday = person_info.find_all('p')[0].text
    authorization = person_info.find_all('p')[1].text
    term_of_office = person_info.find_all('p')[2].text

    person_biography = soup.find('div', class_='person__biography')
    edu_container = person_biography.find_all('div', class_='biography_block')[0]
    edu_p = edu_container.find_all('p')
    edu_count = 0
    edu_list = []
    for p in edu_p:
        edu_item = edu_p[edu_count].text
        edu_list += [edu_item, ]
        edu_count += 1
    region = soup.find('a', class_='region_name_link').text

    data = {'name': name.text,
            'image': image['src'],
            'description': description.strip().replace('\n', ''),
            'educations_list': edu_list,
            'region': region,
            'birthday': birthday.replace('Дата рождения: ', ''),
            'authorization': authorization.replace('\n', '').strip().replace('Дата наделения полномочиями:                        ', ''),
            'term_of_office': term_of_office.replace('\n', '').strip().replace('Срок окончания полномочий                        *:                        ', ''),
            'educations_list': edu_list,}
    return data


def main():
    for url in test_id:
        html = get_html(url)
        data = get_page_data(html)
        if not Elect.objects.filter(name=data["name"]).exists():
            new_elect = Elect.objects.create(
                                                name=data["name"],
                                                description=data["description"],
                                                birthday=data["birthday"],
                                                authorization=data["authorization"],
                                                term_of_office=data["term_of_office"]
                                            )
            region = Region.objects.get(name=data["region"])
            region.elect_region.add(new_elect)

            new_elect.get_remote_image(data["image"])
            
            list = AuthorityList.objects.get(slug="senat")
            list.elect_list.add(new_elect)

            for edu_item in data["educations_list"]:
                EducationElect.objects.create(elect=new_elect, title=edu_item.text[:6], year=edu_dt[edu_count].text[5:])
            print(data["name"])

if __name__ == '__main__':
    main()
