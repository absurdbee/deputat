import sys,os
project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from users.model.profile import *
from users.model.settings import *

try:
    UserNotifications.objects.create(user_id=1)
except:
    pass
try:
    UserPrivate.objects.create(user_id=1)
except:
    pass
try:
    UserInfo.objects.create(user_id=1)
except:
    pass
