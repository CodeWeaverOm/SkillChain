# app/templatetags/dict_extras.py
from django import template

register = template.Library()

@register.filter
def key(d, k):
    """Safely get dict value"""
    try:
        return d.get(k, 0)
    except:
        return 0
