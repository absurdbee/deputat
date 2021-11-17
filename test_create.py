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
from users.models import User
from django.utils.formats import localize
from datetime import date



user = User.objects.get(pk=1)
today = date.today()
age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
print ( str(localize(self.birthday)) + " (" + str(age) + ")")
