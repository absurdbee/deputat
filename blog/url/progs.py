from django.conf.urls import url
from blog.view.progs import *


urlpatterns = [
    url(r'^add_blog/$', BlogCreateView.as_view()),
    url(r'^edit_blog/$', BlogEditView.as_view()),
    url(r'^suggest_elect_new/$', SuggestElectNew.as_view()),
    url(r'^edit_elect_new/(?P<pk>\d+)/$', EditElectNew.as_view()),
    url(r'^edit_manager_elect_new/(?P<pk>\d+)/$', EditManagerElectNew.as_view()),
    url(r'^delete_elect_new/(?P<pk>\d+)/$', DeleteElectNew.as_view()),
    url(r'^restore_elect_new/(?P<pk>\d+)/$', RestoreElectNew.as_view()),
]
