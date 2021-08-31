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
print (len(data))
print (len(data[0]), data[0][0], data[0][1], data[0][2], data[0][3])
print (data[0][0])
print (data[0][1])
print (data[0][2])
print (data[0][3])

#for region in Region.objects.all():
#    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + region.name)
#    data = response.json()
#    print (data)
