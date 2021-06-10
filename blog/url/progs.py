from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^suggest_elect_new/$', SuggestElectNew.as_view()),
    url(r'^edit_elect_new/$', EditElectNew.as_view()),
    url(r'^delete_elect_new/$', DeleteElectNew.as_view()),
    url(r'^restore_elect_new/$', RestoreElectNew.as_view()),
]
