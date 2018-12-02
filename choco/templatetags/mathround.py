from django import template

register = template.Library()


@register.filter
def mathround(value, arg):
    """Rounds value to arg digits after dot"""
    try:
        return round(value, arg)
    except (ValueError, TypeError):
        return -1
