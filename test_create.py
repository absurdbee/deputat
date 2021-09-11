import sys,os
project_dir = '../deputat/deputat/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from users.model.profile import *
from users.model.settings import *
from elect.models import Elect
from gallery.models import Photo

print('<img src="' + Photo.objects.get(pk=647).file + '>')
