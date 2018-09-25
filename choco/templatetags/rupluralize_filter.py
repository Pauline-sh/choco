from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def rupluralize(value, forms):
    try:
        one, two, many = forms.split(u',')
        value = str(value)[-2:]  # 314 -> 14

        if 21 > int(value) > 4:
            return many

        if value.endswith('1'):
            return one
        elif value.endswith(('2', '3', '4')):
            return two
        else:
            return many

    except (ValueError, TypeError):
        return ''
