import sys,os
import re
import requests
import time
from bs4 import BeautifulSoup

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from common.model.other import *

test_id = ['http://council.gov.ru/structure/persons/1317/', ]
sity_names = ['г.Москва', 'г.Санкт-Петербург', 'г.Севастополь', ]

def get_html(url):
    r = requests.get(url)
    return r.text

def main():
    html = get_html("https://kody-smajlov-vkontakte.ru/#gestures")

    soup = BeautifulSoup(html, 'lxml')
    con = soup.find('div', class_='container')
    blocks = con.find_all('table', class_='smile_table')
    order = 0

    for block in blocks:
        order += 1
        cat_name = block.find('div', class_='head_str').text
        if SmileCategory.objects.filter(name=cat_name).exists():
            category = SmileCategory.objects.get(name=cat_name)
        else:
            category = SmileCategory.objects.create(name=cat_name, order=order)
        items = block.find_all('tr')
        tr_count = 0
        for item in items:
            if tr_count > 0:
                tr_count += 1
                name = item.find('td', class_='description').text
                try:
                    image_src = "https://kody-smajlov-vkontakte.ru/" + item.find('img')['src']
                except:
                    image_src = None

                if Smile.objects.filter(name=name).exists():
                    pass
                else:
                    smile = Smile.objects.create(name=name, order=tr_count)
                    try:
                        smile.get_remote_image(image_src)
                    except:
                        pass

if __name__ == '__main__':
    main()
