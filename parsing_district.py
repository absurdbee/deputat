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
data_city_includes = ["поселение", "сельсовет", "наслег"]


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

        if path_0 in data_district_includes:
            if not District.objects.filter(name=path_0, region=region).exists():
                District.objects.create(name=path_0, region=region, link=data[count][2])
                print ("District создан!")
        elif path_1 in data_district_includes:
            if not District.objects.filter(name=path_0, region=region).exists():
                District.objects.create(name=path_0, region=region, link=data[count][2])
                print ("District создан!")
        if not city_or_district in data_district_includes:
            if not City.objects.filter(name=city_or_district, region=region).exists():
                City.objects.create(name=city_or_district, region=region, link=data[count][2])
                print ("City создан!")
            else:
                city = City.objects.get(name=city_or_district, region=region)
                city.link = data[count][2]
                city.save(update_fields=["link"])
                print ("City присвоена ссылка!")

        #if len(path) == 3:
        #    print ("дистрикт: ", path_1)
        #    path_2 = path[2].replace("город ", "")
        #    print ("регион: ", path_2)
        #elif len(path) == 2:
        #    print ("регион: ", path_1)

        #print ("ссылка ", data[count][2])
        count += 1
        print ("-----------------")
    print ("==============================")
    break
