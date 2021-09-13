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



for elect in Elect.objects.all():
    elect.vk = ""
    elect.fb = ""
    elect.ig = ""
    elect.tg = ""
    elect.tw = ""
    elect.mail = ""
    elect.phone = ""
    elect.address = ""
    elect.save()
