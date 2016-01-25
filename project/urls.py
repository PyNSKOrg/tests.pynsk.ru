# -*- encoding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tgmbot.urls')),
    url(r'^', include('testapp.urls', namespace='pages')),
]