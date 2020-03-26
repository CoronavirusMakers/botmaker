import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convierte(s):
    return re.sub(r'(\/\w+)', r'<a href="/estatico\1">\1</a>', s)
