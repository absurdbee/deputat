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

query = Q(slug="candidate_municipal")|Q(slug="candidate_duma")

lists = AuthorityList.objects.filter(query)

elects = Elect.objects.all()
for elect in elects:
    if Elect.objects.filter(name=elect.name).values("pk").count > 2:
        print (" Двойники: ")
        for el in Elect.objects.filter(name=elect.name):
            print ( el.name , ", ", el.list)
