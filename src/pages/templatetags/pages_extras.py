import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def convert(s):
    out = re.sub(r'(\/\w+)', r'<a href="/pages\1">\1</a>', s)
    return mark_safe(out)
