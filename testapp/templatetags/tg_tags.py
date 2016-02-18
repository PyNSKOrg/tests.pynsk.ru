# -*- encoding: utf-8 -*-

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def bot_name():
    return '@{}'.format(settings.TGM_BOT_NAME)


@register.simple_tag()
def bot_raw_name():
    return settings.TGM_BOT_NAME


@register.simple_tag()
def bot_url(text=None):
    name = settings.TGM_BOT_NAME
    if text is None:
        text = "@{}".format(name)
    return '<a href="https://telegram.me/{}" target="_blank">{}</a>'.format(name.lower(), text)
