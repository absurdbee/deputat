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
data_district_includes = ["сельсовет", "район"]


from region.models import Region

for region in Region.objects.all():
    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + region.name)
    data = response.json()
    count = 0
    for i in data:
        print ("кол-во дистриктов/городов", len(data[count]))
        print ("полный путь ", data[count][0])

        path = data[count][0].split(",")

        print ("единица ", path[0])
        path_1 = path[1].replace("город ", "")
        if len(path) == 3:
            print ("дистрикт ", path_1)
            path_2 = path[2].replace("город ", "")
            print ("регион ", path_2)
        else:
            print ("регион ", path_1)

        print ("ссылка ", data[count][2])
        count += 1
    break
