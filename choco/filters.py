import django_filters
from django import forms
from django.db.models import Max, Min

class RangeInput(forms.widgets.NumberInput):
    input_type = 'range'
