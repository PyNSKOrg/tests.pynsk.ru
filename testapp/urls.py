# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, url

from testapp.views import ThanksPage, AboutPage, IndexPage, RatingPage, HowToWorkPage, TestsPage, TestDetailPage

urlpatterns = patterns(
    '',
    url(r'^thanks$', ThanksPage.as_view(), name='thanks'),
    url(r'^about$', AboutPage.as_view(), name='about'),
    url(r'^rating$', RatingPage.as_view(), name='rating'),
    url(r'^howto$', HowToWorkPage.as_view(), name='howtowork'),

    url(r'^tests$', TestsPage.as_view(), name='tests'),
    url(r'^test/(?P<pk>[-\w]+)/$', TestDetailPage.as_view(), name='test-detail'),

    url(r'^$', IndexPage.as_view(), name="home"),

)
