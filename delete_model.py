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

from common.model.votes import ElectRating
from elect.models import Elect

if ElectRating.objects.filter(elect_id=178, user_id=1).exists():
    rat = ElectRating.objects.get(elect_id=178, user_id=1)
    rat.vakcine = -5
    rat.pp_825 = 5
    rat.safe_family = 0
    rat.pro_life = 2
    rat.free_vacation = 1
    rat.save()
else:
    rat = ElectRating.objects.create(elect_id=178, user_id=1)
    rat.vakcine = -5
    rat.pp_825 = 5
    rat.safe_family = 0
    rat.pro_life = 2
    rat.free_vacation = 1
    rat.save()
