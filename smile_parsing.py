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

url_list = [
    'https://vkclub.su/ru/emojis/sets/emotions/',
    'https://vkclub.su/ru/emojis/sets/body%20parts/',
    'https://vkclub.su/ru/emojis/sets/gestures/',
    'https://vkclub.su/ru/emojis/sets/cat%20emotions/',
    'https://vkclub.su/ru/emojis/sets/mugs/',
    'https://vkclub.su/ru/emojis/sets/letters-words-symbols/',
    'https://vkclub.su/ru/emojis/sets/numbers/',
    'https://vkclub.su/ru/emojis/sets/faces/',
    'https://vkclub.su/ru/emojis/sets/animals-fishes-insects/',
    'https://vkclub.su/ru/emojis/sets/weather/',
    'https://vkclub.su/ru/emojis/sets/phones-pagers/',
    'https://vkclub.su/ru/emojis/sets/music-musical-instruments/',
    'https://vkclub.su/ru/emojis/sets/volume-speaker/',
    'https://vkclub.su/ru/emojis/sets/buildings/',
    'https://vkclub.su/ru/emojis/sets/sports/',
    'https://vkclub.su/ru/emojis/sets/holiday/',
    'https://vkclub.su/ru/emojis/sets/flowers/',
    'https://vkclub.su/ru/emojis/sets/food-drinks/',
    'https://vkclub.su/ru/emojis/sets/clothes-footwear-accessories/',
    'https://vkclub.su/ru/emojis/sets/heart-love-decorations/',
    'https://vkclub.su/ru/emojis/sets/money-rates/',
    'https://vkclub.su/ru/emojis/sets/office/',
    'https://vkclub.su/ru/emojis/sets/lock/',
    'https://vkclub.su/ru/emojis/sets/instruments/',
    'https://vkclub.su/ru/emojis/sets/transport/',
    'https://vkclub.su/ru/emojis/sets/mail/',
    'https://vkclub.su/ru/emojis/sets/sun-earth-moon-stars/',
    'https://vkclub.su/ru/emojis/sets/landscapes/',
    'https://vkclub.su/ru/emojis/sets/trees-plants-leaves/',
    'https://vkclub.su/ru/emojis/sets/arrows/',
    'https://vkclub.su/ru/emojis/sets/clock/',
    'https://vkclub.su/ru/emojis/sets/shapes/',
    'https://vkclub.su/ru/emojis/sets/signs/',
    'https://vkclub.su/ru/emojis/sets/zodiac/',
    'https://vkclub.su/ru/emojis/sets/movie/',
    'https://vkclub.su/ru/emojis/sets/card%20suits/',
    'https://vkclub.su/ru/emojis/sets/flags/',
    'https://vkclub.su/ru/emojis/sets/various/',
]

def get_html(url):
    r = requests.get(url)
    return r.text

def main():
    order = 0
    for url in url_list:
        order += 1
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')

        con = soup.find("section", class_='page')
        cat_name = con.find('h1').text
        if SmileCategory.objects.filter(name=cat_name).exists():
            category = SmileCategory.objects.get(name=cat_name)
        else:
            category = SmileCategory.objects.create(name=cat_name, order=order)
        print("category", category)
        block = con.find("div", class_='emojicat_list')
        items = block.find_all('div', class_='image')
        tr_count = 0
        for item in items:
            tr_count += 1
            name = item.find('a')['title']
            image_src = item.find('img')['src']
            print(name)
            print(image_src)

            #if Smile.objects.filter(name=name).exists():
            #    pass
            #else:
            #    smile = Smile.objects.create(name=name, order=tr_count)
            #    smile.get_remote_image(image_src)
            time.sleep(2)

if __name__ == '__main__':
    main()
