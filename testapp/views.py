# -*- encoding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView

from testapp.models import Test


class ThanksPage(TemplateView):
    template_name = 'pages/thanks.html'


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class HowToWorkPage(TemplateView):
    template_name = 'pages/howtowork.html'


class TestsPage(ListView):
    model = Test


class TestDetailPage(DetailView):
    model = Test


class RatingPage(TemplateView):
    template_name = 'pages/rating.html'


class DonatePage(TemplateView):
    template_name = 'pages/donate.html'


class IndexPage(TemplateView):
    template_name = 'home.html'
