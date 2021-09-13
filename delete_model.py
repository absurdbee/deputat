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
    if elect.vk == "None":
        elect.vk = ""
    if elect.fb == "None":
        elect.fb = ""
    if elect.ig == "None":
        elect.ig = ""
    if elect.tg == "None":
        elect.tg = ""
    if elect.tw == "None":
        elect.tw = ""
    if elect.mail == "None":
        elect.mail = ""
    if elect.phone == "None":
        elect.phone = ""
    if elect.address == "None":
        elect.address = ""
    elect.save()
