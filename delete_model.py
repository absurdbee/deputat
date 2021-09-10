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
    try:
        if elects.filter(name=elect.name).values("pk").count() > 1:
            if copy_birthday(elects.filter(name=elect.name)):
                e = elects.filter(name=elect.name)[0]
                for el in elects.filter(name=elect.name):
                    try:
                        e.okrug.add(el.area.all()[0])
                        if el.pk != e.pk:
                            el.delete()
                            print (el.okrug.all()[0])
                        print("Округ добавлен, человек удален")
                    except:
                        if el.pk != e.pk:
                            el.delete()
                            print("Округа нет, человек удален")
    except:
        pass
