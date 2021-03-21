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

def get_links(url):
    soup = BeautifulSoup(url, 'lxml')
    list = []
    container = soup.find('section', class_='list-persons__wrapper js-deputies-wrapper')
    blocks = container.find_all('a', class_='person__image-wrapper person__image-wrapper--s')
    for item in blocks:
        list += ['http://duma.gov.ru' + item['href'], ]
    return list


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    # name
    name = soup.find('h1', class_='article__title--person')
    if name:
        _name = str(name)
        _name = _name.replace('\n', '').replace('<h1 class="article__title article__title--person">', '').replace('<br/>', ' ').replace('</h1>', '')
    else:
        name = soup.find('h2', class_='person__title person__title--l')
        _name = str(name)
        _name = _name.replace('\n', '').replace('<h2 class="person__title person__title--l"><span itemprop="name">', '').replace('<br/>', ' ').replace('</span></h2>', '').replace('</h2>', '')

    try:
        region_list = soup.find_all('div', class_='person__description__col')[3].text.replace(", ", ",")
    except:
        region_list = []

    data = {'name': _name, 'region_list': region_list}
    return data


def main():
    html = get_html("http://duma.gov.ru/duma/deputies/")
    lists = get_links(html)
    for url in lists:
        html = get_html(url)
        data = get_page_data(html)

        elect = Elect.objects.get(name=data["name"])
        regions_query = data["region_list"]
        if regions_query:
            regions_query = data["region_list"].split(",")
            for region_name in regions_query:
                try:
                    region = Region.objects.get(name=region_name)
                    region.elect_region.add(elect)
                    print(data["name"])
                except:
                    pass
        print("not ok")

if __name__ == '__main__':
    main()
