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
print (data)

#for region in Region.objects.all():
#    response = requests.get(url= "https://election.novayagazeta.ru/api/address/?address=" + region.name)
#    data = response.json()
#    print (data)
