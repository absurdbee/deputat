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

for city in City.objects.all():
    #_name = city.name.replace("поселок ", "").replace("округ ", "")
    #city.name = _name
    #city.save(update_fields=["name"])
    if "муниципальный" in city.name:
        city.delete()
        print ("Deleted!")
