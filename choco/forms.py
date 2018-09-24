from django import forms
from .models import Assortment


class CartAddProductForm(forms.Form):
    PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)]
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
