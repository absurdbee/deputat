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
from blog.models import ElectNew
from lists.models import AuthorityList
from django.db.models import Q

count = 0
deputat_list = AuthorityList.objects.get(slug="state_duma")
candidate_list = AuthorityList.objects.get(slug="candidate_duma")

lists = Q(list__slug="candidate_duma")|Q(list__slug="state_duma")

for elect in Elect.objects.filter(list=deputat_list):
    if elect.list.all().count() > 1:
        count += 1
        print("прогон ", count)
        #print(elect, " Старый")
