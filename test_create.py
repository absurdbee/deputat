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
from logs.model.manage_elect_new import ElectNewManageLog

for log in ElectNewManageLog.objects.all():
    if log.action_type == 'CCLO':
        log.action_type == 'IPUB'
        log.save(update_fields=["action_type"])
