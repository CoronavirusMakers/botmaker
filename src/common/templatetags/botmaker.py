import re
import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def convert_slash_to_nodes(s):
    # FIXME la regex no soporta un /cosa al principio, pero si ignora los http://tal
    out = re.sub(r'(\s)(\/\w+)\b', r'\1<a href="\2">\2</a>', s)
    return mark_safe(out)


@register.filter
@stringfilter
def convert_markdown(s):
    out = markdown.markdown(s)
    return mark_safe(out)


@register.filter
@stringfilter
def quote_telegram(s):
    return s.replace("_", "\\_")
