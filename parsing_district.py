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


""" Определим слова для понимания - в поле город или район?
    Если вхождение есть со списком data_district_includes, значит это район
"""
data_district_includes = ["район", "округ"]


from region.models import Region
from district.models import District
from city.models import City

for region in Region.objects.all():
    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + region.name)
    data = response.json()
    count = 0
    for i in data:
        path = data[count][0].split(",")
        path_0 = path[0].replace("город ", "")
        path_1 = path[1].replace("город ", "")

        city_or_district = data[count][1]

        if not "район" in city_or_district or "округ" in city_or_district:
            if City.objects.filter(name=city_or_district, region=region).exists():
                city = City.objects.get(name=city_or_district, region=region)
                if not city.link:
                    city.link = data[count][2]
                    city.save(update_fields=["link"])
                    print ("City присвоена ссылка!")
        count += 1
        print ("-----------------")
    print ("==============================")
