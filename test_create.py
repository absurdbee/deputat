import sys,os
project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from users.model.profile import *
from users.model.settings import *
from elect.models import Elect
from blog.models import ElectNew

for elect in Elect.objects.filter(list__slug="candidate_municipal"):
    if ElectNew.objects.filter(elect=elect):
        print ("Чиновник имеет активности", elect)
