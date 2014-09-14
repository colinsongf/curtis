from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from qa import views

urlpatterns = patterns('',url(r'^$',views.index,name='index'),url(r'^q/(?P<qtext>.+)/?$',views.question,name='ask'),)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

#url(r'^(?P<qtext>(\w|\s)/?$',views.question,name='ask')