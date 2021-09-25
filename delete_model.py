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

from elect.models import Elect
from lists.models import AuthorityList
from django.db.models import Q


count = 0
for elect in Elect.objects.all():

    if Elect.objects.filter(name=elect.name, list__slug="candidate_municipal").values("pk").count() > 1:
        count += 1
        print("---------- Прогон ", count, "-----------")
        for i in Elect.objects.filter(name=elect.name):
            print("Имя: " , i.name,  " | Возраст: " , i.birthday,  " | Список: " , i.get_first_list())
