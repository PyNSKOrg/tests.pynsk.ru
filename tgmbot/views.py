# -*- encoding: utf-8 -*-

import telebot
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from .bot import bot


def webhook(request):
    if request.method == 'POST':
        if request.META['CONTENT_TYPE'] == 'application/json':
            json_string = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_messages([update.message])
            return HttpResponse()

    raise PermissionDenied
