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

"""
    1. Белгородская область - районы
    2. Волгоградская область - районы
    3. Кабардино-Балкарская область - районы
    4. Калининградская область - районы
    5. Костромская область - районы
    6. Ленинградская область - районы
    7. Липецкая область - районы
    8. Магаданская область - районы
    9. Московская область - районы
    10. Новгородская область - районы
    11. Орловская область - районы
    12. Республика Дагестан - районы
    13. Республика Ингушетия - районы
    14. Республика Карелия - районы
    15. Республика Крым - районы
    16. Ростовская область - районы
    17. Рязанская область - районы
    18. Самарская область - районы
    19. Тульская область - районы

    20. Удмуртская Республика - районы
    21. Ульяновкая область - районы
    22. Ханты-Мансийский - районы
    23. Ярославская область - районы
"""
""" Определим слова для понимания - в поле город или район?
    Если вхождение есть со списком data_district_includes, значит это район
"""
data_district_includes = ["район", "округ"]


from region.models import Region
from district.models import District
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
        path = data[count][0].split(",")
        if len(path) > 2:
            path_1 = path[0]
            path_2 = path[1]
            path_3 = path[3]
            if not City.objects.filter(name=path_1, region=region).exists():
                City.objects.create(name=path_1, region=region, link=data[count][2])
            if not District.objects.filter(name=path_2, region=region).exists():
                District.objects.create(name=path_2, region=region, link=data[count][2])
        else:
            city_or_district = data[count][1]

            if not "район" in city_or_district and not "округ" in city_or_district:
                if not City.objects.filter(name=city_or_district, region=region).exists():
                    City.objects.create(name=city_or_district, region=region, link=data[count][2])
            else:
                if not District.objects.filter(name=city_or_district, region=region).exists():
                    District.objects.create(name=city_or_district, region=region, link=data[count][2])
        count += 1
        print ("-----------------")
    print ("==============================")
