from django.conf.urls import url
from quan.views import *


urlpatterns = [
    url(r'^(?P<cat_name>[\w\-]+)/$', QuanCategoryView.as_view(), name='quan_categories'),
    url(r'^$', QuanView.as_view(), name='quan'),
    url(r'^who_to_contact/$', WhoContactView.as_view()),
    url(r'^how_to_apply/$', HowApplyView.as_view()),
    url(r'^where_to_apply/$', WhereApplyView.as_view()),
    url(r'^why_publish/$', WhyPublishView.as_view()),
    url(r'^how_to_publish/$', HowPublishView.as_view()),
]
