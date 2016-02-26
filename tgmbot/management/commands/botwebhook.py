# -*- encoding: utf-8 -*-

import telebot
from django.conf import settings
from django.core.management.base import BaseCommand

"""
add
TGM_SSL_SERT = get_secret('tgm_ssl_sert')
in settings.py
"""


class Command(BaseCommand):
    help = 'Run bot'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Start webhook bot...")

        WEBHOOK_HOST = 'tests.pynsk.ru'
        WEBHOOK_PORT = 443
        WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
        WEBHOOK_URL_PATH = "/%s/" % settings.TGM_BOT_TOKEN
        bot = telebot.TeleBot(settings.TGM_BOT_TOKEN)
        bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(settings.TGM_SSL_SERT, 'r'))
        bot.polling()
        print("Stop webhook bot...")
