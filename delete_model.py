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
new_list = AuthorityList.objects.get(slug="state_duma_21_26")

lists = Q(list__slug="state_duma") | Q(list__slug="state_duma_21_26")
elects = Elect.objects.filter(lists)

for elect in elects:
    if elects.filter(name=elect.name).count() > 1:
        print("Есть совпедение", elect.name)
        if not ElectNew.objects.filter(elect=elect).exists() and elect.list == new_list:
            elect.delete()

    print("---------------")
