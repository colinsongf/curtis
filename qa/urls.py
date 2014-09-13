from django.conf.urls import patterns, url

from qa import views

urlpatterns = patterns('',url(r'^$',views.index,name='index'),url(r'^q/(?P<qtext>.+)/?$',views.question,name='ask'),)

#url(r'^(?P<qtext>(\w|\s)/?$',views.question,name='ask')