from django.conf.urls import url
from stst.views import StatView


urlpatterns = [
    url(r'^$', StatView.as_view(), name='stat'),

    url(r'^elect_year/(?P<pk>[0-9]+)/$', ElectYearStat.as_view(), name='elect_year_stat'),
    #url(r'^elect_month/(?P<pk>[0-9]+)/$', ElectMonthStat.as_view(), name='elect_month_stat'),
    #url(r'^elect_week/(?P<pk>[0-9]+)/$', ElectWeekStat.as_view(), name='elect_week_stat'),
    #url(r'^elect_day/(?P<pk>[0-9]+)/$', ElectDayStat.as_view(), name='elect_day_stat'),

    #url(r'^blog_year/(?P<pk>[0-9]+)/$', BlogYearStat.as_view(), name='blog_year_stat'),
    #url(r'^blog_month/(?P<pk>[0-9]+)/$', BlogMonthStat.as_view(), name='blog_month_stat'),
    #url(r'^blog_week/(?P<pk>[0-9]+)/$', BlogWeekStat.as_view(), name='blog_week_stat'),
    #url(r'^blog_day/(?P<pk>[0-9]+)/$', BlogDayStat.as_view(), name='blog_day_stat'),

    #url(r'^elect_new_year/(?P<pk>[0-9]+)/$', ElectNewYearStat.as_view(), name='elect_new_year_stat'),
    #url(r'^elect_new_month/(?P<pk>[0-9]+)/$', ElectNewMonthStat.as_view(), name='elect_new_month_stat'),
    #url(r'^elect_new_week/(?P<pk>[0-9]+)/$', ElectNewWeekStat.as_view(), name='elect_new_week_stat'),
    #url(r'^elect_new_day/(?P<pk>[0-9]+)/$', ElectNewDayStat.as_view(), name='elect_new_day_stat'),
]
