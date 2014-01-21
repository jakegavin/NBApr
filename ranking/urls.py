from django.conf.urls import patterns, url

from ranking import views 

urlpatterns = patterns('', 
        url(r'^$', views.AvgRankingView, name='avgrank'),
    )