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

response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + "Коми")
data = response.json()
print ("кол-во элементов ", len(data))
print ("кол-во ", len(data[0]))
print ("полный путь ", data[0][0])

path = data[0][0].split(",")

print ("единица ", path[0])
if len(path) == 3:
    print ("дистрикт ", path[1])
    print ("регион ", path[2])
else:
    print ("регион ", path[1])

print ("ссылка ", data[0][2])

for region in Region.objects.all():
    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + region.name)
    data = response.json()
    for i in len(data):
        print ("кол-во дистриктов/городов", len(data[i]))
        print ("полный путь ", data[i][0])

        path = data[i][0].split(",")

        print ("единица ", path[0])
        if len(path) == 3:
            print ("дистрикт ", path[1])
            print ("регион ", path[2])
        else:
            print ("регион ", path[1])

        print ("ссылка ", data[i][2])
        break
