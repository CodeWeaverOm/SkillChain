from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Safely get value from dict in templates."""
    if dictionary and key in dictionary:
        return dictionary[key]
    return None

@register.filter
def to_list(value, max_value):
    """Return a list of integers from value to max_value (inclusive)."""
    return range(value, max_value + 1)
