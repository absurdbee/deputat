import sys,os
import re
import requests
import time
from bs4 import BeautifulSoup

project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from lists.models import *
from elect.models import *

def main():
    _list = AuthorityList.objects.get(slug="zaks_2021")
    for elect in Elect.objects.filter(list=_list):
        print("чиновник -", elect.name)

if __name__ == '__main__':
    main()
