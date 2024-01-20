from django import template

from config import settings

register = template.Library()


@register.simple_tag
def mediapath(sub_url):
    return settings.MEDIA_URL + str(sub_url)


@register.filter
def mediapath_filter(sub_url):
    return settings.MEDIA_URL + str(sub_url)

