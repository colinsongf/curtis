from django.conf import settings
from django.conf.urls import patterns, include, url,static
from django.contrib import admin


urlpatterns = patterns('',
	url(r'^curtis/',include('qa.urls')),
    # Examples:
    # url(r'^$', 'curtis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

#urlpatterns+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
