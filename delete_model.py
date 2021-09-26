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

deputat_list = AuthorityList.objects.get(slug="state_duma")
candidate_list = AuthorityList.objects.get(slug="candidate_duma")

count = 0
lists = Q(list__slug="candidate_duma")|Q(list__slug="state_duma")

for elect in Elect.objects.all():
    if Elect.objects.filter(lists, name=elect.name).values("pk").count() > 1:
        count += 1
        print("---------- Прогон ", count, "-----------")

        #берем обе копии депутата - одна в госдуме, вторая - новый кандидат
        elects = Elect.objects.filter(lists, name=elect.name)
        if elects[0].get_first_list() == deputat_list:
            current_elect = elects[0]
            delete_elect = elects[1]
        else:
            current_elect = elects[1]
            delete_elect = elects[0]

        # депутату из думы присваиваем новый список, ведь он теперь и депутат
        current_elect.list.add(candidate_list)

        # а это депутат, которого будем удалять, но сначала нам надо найти все активности с ним связанные,
        # и записать их на старого депутата, чтобы они не потерялись

        news = ElectNew.objects.filter(elect=delete_elect)
        for new in news:
            new.elect = current_elect
            new.save(update_fields=["elect"])
            print("Активность получила нового депутата!")

        delete_elect.old = True
        delete_elect.save(update_fields=["old"])
        print("Копия помечена!")
