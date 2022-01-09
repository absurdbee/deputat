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

def get_html(url):
    r = requests.get(url)
    return r.text

def main():
    html = get_html("https://www.dmosk.ru/skachka.php?smiles=all")

    soup = BeautifulSoup(html, 'lxml')
    con = soup.find("table", class_='main')
    print("con", con)
    blocks = con.find_all('div', class_='cat-wrapper')
    order = 0
    print("Блоки", blocks)

    for block in blocks:
        order += 1
        cat_name = block.find('h1').text
        print("Название", cat_name)
        if SmileCategory.objects.filter(name=cat_name).exists():
            category = SmileCategory.objects.get(name=cat_name)
        else:
            category = SmileCategory.objects.create(name=cat_name, order=order)
        items = block.find_all('span')
        tr_count = 0
        for item in items:
            print("item")
            tr_count += 1
            if tr_count > 0:
                name = item.find('a')['title']
                try:
                    image_src = item.find('img')['src']
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
