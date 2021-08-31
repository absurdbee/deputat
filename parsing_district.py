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
print ("кол-во элементов "len(data))
print ("кол-во " len(data[0]), ";полный путь " data[0][0], ";единица " data[0][1], ";ссылка " data[0][2], ";число какое то " data[0][3])

#for region in Region.objects.all():
#    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + region.name)
#    data = response.json()
#    print (data)
