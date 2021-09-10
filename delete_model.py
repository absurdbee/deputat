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

def copy_birthday(list):
    old = list[0].birthday
    for i in list:
        if not i.birthday == old:
            return False
    return True

elects = Elect.objects.filter(list__slug="candidate_municipal")
for elect in elects:
    if elects.filter(name=elect.name).values("pk").count() > 2:
        if copy_birthday(elects.filter(name=elect.name)):
            e = elects.filter(name=elect.name)[0]
            print (e)
            for el in elects.filter(name=elect.name):
                try:
                    e.area.add(el.area.all()[0])
                    el.delete()
                    print (el.area.all()[0])
                except:
                    el.delete()
