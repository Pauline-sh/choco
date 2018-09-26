# -*- coding: utf-8 -*-
from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label="", initial=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderForm(forms.Form):
    name = forms.CharField(label="Имя*")
    city = forms.CharField(label="Город", required=False)
    phone_number = forms.CharField(label="Контактный телефон*", widget=forms.TextInput(attrs={'placeholder': '+7(999)999-99-99'}))
    note = forms.CharField(label="Дополнительная информация", widget=forms.Textarea(), required=False)


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя*")
    email = forms.CharField(label="E-mail*")
    subject = forms.CharField(required=False, label="Тема сообщения")
    message = forms.CharField(label="Текст сообщения*", widget=forms.Textarea())
