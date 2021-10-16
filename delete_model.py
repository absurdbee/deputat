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
    # если есть двойники (их не больше 2)
    if elects.filter(name=elect.name).count() > 1:
        count += 1
        print(count)
        print(elect.name)
        # если у этого чиновника есть активности и он с нового списка
        if ElectNew.objects.filter(elect=elect).exists() and new_list in elect.get_lists():
            # получаем старого чиновника
            _elect = elects.filter(name=elect.name, list=deputat_list)
            # все активности нового переводим на стпрого
            for new in ElectNew.objects.get(elect=elect):
                new.elect = _elect
                new.save(update_fields=["elect"])
            # удаляем чиновника
            #elect.delete()
        # если у чиновника нет активностей и он с нового списка, то удаляем его
    if not ElectNew.objects.filter(elect=elect).exists() and new_list in elect.get_lists():
        elect.delete()

    print("---------------")
