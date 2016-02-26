# -*- encoding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def menu_element(context, url, title, icon_class=''):
    label = 'active' if 'request' in context and url == context['request'].get_full_path() else ''
    return """<li class="nav-item {2}">
                <a class="nav-link" href="{0}"><i class="fa {3}"></i>{1}</a>
            </li>""".format(
        url,
        title,
        label,
        icon_class,
    )


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
