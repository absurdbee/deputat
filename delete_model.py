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

if ElectRating.objects.filter(elect_id=178).exists():
    rat = ElectRating.objects.get(elect_id=178)
    rat.vakcine = -5
    rat.save(update_fields=["vakcine"])
else:
    rat = ElectRating.objects.create(elect_id=178)
    rat.vakcine = -5
    rat.save(update_fields=["vakcine"])
