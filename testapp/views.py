# -*- encoding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView

from testapp.models import Test, Player, ResultView


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


class RatingPage(ListView):
    model = ResultView
    template_name = 'pages/rating.html'

    def get_queryset(self):
        return ResultView.objects.order_by('test')

    def get_context_data(self, **kwargs):
        context = super(RatingPage, self).get_context_data(**kwargs)
        context['players'] = {x.id: x for x in Player.objects.all()}
        context['tests'] = {x.id: x for x in Test.objects.filter(published=True)}
        return context
        #
        # # мне надо
        # взять всех пользователей
        # взять все тесты
        #
        # для каждого теста получить пользователя и его рейтинг


class DonatePage(TemplateView):
    template_name = 'pages/donate.html'


class IndexPage(TemplateView):
    template_name = 'home.html'
