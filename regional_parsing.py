import sys,os
import re
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from city.models import City

city_with_link = 0
city_no_link = 0

for city in City.objects.all():
    if city.link:
        city_with_link += 1
    else:
        city_no_link += 1

print ("Город со ссылкой ", city_with_link)
print ("Город без ссылки ", city_no_link)
