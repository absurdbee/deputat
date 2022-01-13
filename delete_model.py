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
from managers.models import Moderated
from django.db.models import Q
from common.model.other import *


for elect in Elect.objects.all():
    name = elect.name.replace("ё", "е").replace("Ё", "Е")
    elect.name = name
    elect.save(update_fields=["name"])
