# -*- encoding: utf-8 -*-

from django.core.management.base import BaseCommand
from tgmbot.bot import bot


class Command(BaseCommand):
    help = 'Run bot'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Start bot...")
        bot.polling(none_stop=True)
        print("Stop bot...")
