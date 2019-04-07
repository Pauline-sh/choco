# -*- coding: utf-8 -*-
from django import forms
from .models import Assortment, Configuration


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="", initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    configuration = forms.ModelChoiceField(required=False, queryset=Configuration.objects.all())
    old_configuration = forms.ModelChoiceField(required=False, initial=None, queryset=Configuration.objects.all())

    def __init__(self, item_id=-1, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        if item_id != -1:
            self.fields['configuration'].queryset = Assortment.objects.get(pk=item_id).choco_config.all()


class GiftAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="", initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    configuration = forms.ModelChoiceField(required=False, queryset=Configuration.objects.all())
    old_configuration = forms.ModelChoiceField(required=False, initial=None, queryset=Configuration.objects.all())

    def __init__(self, item_id=-1, *args, **kwargs):
        super(GiftAddProductForm, self).__init__(*args, **kwargs)
        if item_id != -1:
            self.fields['configuration'].queryset = Assortment.objects.get(pk=item_id).choco_config.all()


class OrderForm(forms.Form):
    name = forms.CharField(label="Имя*")
    city = forms.CharField(label="Город", required=False)
    phone_number = forms.CharField(label="Контактный телефон*", widget=forms.TextInput(attrs={'placeholder': '+7(999)999-99-99'}))
    note = forms.CharField(label="Дополнительная информация", widget=forms.Textarea(), required=False)


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя")
    phone = forms.CharField(label="Телефон", widget=forms.TextInput(attrs={'placeholder': '+7(999)999-99-99'}))
