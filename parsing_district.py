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


from region.models import Region
from district.models import District2
from city.models import City

for region in Region.objects.filter(id__in=[57,37]):
    if region.name == "Удмуртская Республика (Удмуртия)":
        _name = "Удмуртская Республика"
    elif region.name == "Ханты-Мансийский автономный округ - Югра (Тюменская область)":
        _name = "Ханты-Мансийский автономный округ"
    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + _name)
    data = response.json()
    count = 0
    for i in data:
        d = District2.objects.create(name=data[count][1], region=region, link=data[count][2])
        count += 1
        print ("Добавлен дистрикт ", d)
    print ("==============================")
