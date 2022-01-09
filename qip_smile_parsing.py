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
    print("Открываем ссылку")

    soup = BeautifulSoup(html, 'lxml')
    con = soup.find("table")

    if SmileCategory.objects.filter(name="Qip-смайлы").exists():
        category = SmileCategory.objects.get(name="Qip-смайлы")
    else:
        category = SmileCategory.objects.create(name="Qip-смайлы", gif=True)
    items = con.find_all('img')
    for item in items:
        name = "Без названия"
        image_src = "https://www.dmosk.ru/" + item['src']
        smile = Smiles.objects.create(category=category, name=name)
        smile.get_remote_image(image_src)

if __name__ == '__main__':
    main()
