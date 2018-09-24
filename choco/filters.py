import django_filters
from django import forms
from django.db.models import Max, Min

from .models import Assortment

class RangeInput(forms.widgets.NumberInput):
    input_type = 'range'


class AssortmentFilter(django_filters.FilterSet):
    pass
