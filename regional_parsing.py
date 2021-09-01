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
from district.models import District

district_no_link = 0
city_no_link = 0

for city in City.objects.all():
    if not city.link:
        city_no_link += 1
for district in District.objects.all():
    if not district.link:
        district_no_link += 1

print ("Регион без ссылкой ", district_no_link)
print ("Город без ссылки ", city_no_link)
