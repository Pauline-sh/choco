# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.http import HttpResponse

from .models import Assortment
from .cart import Cart
from .forms import CartAddProductForm, OrderForm, ContactForm

EMAIL_FROM = 'pauline-sh-hub@yandex.ru'

def home_page(request):
    return render(request, 'home.html')


def about_page(request):
    return render(request, 'about.html')


def contacts_page(request):
    contact_form = ContactForm()
    return render(request, 'contacts.html', {'contact_form': contact_form})


def details_page(request, pk):
    choco_item = get_object_or_404(Assortment, pk=pk)
    cart_form = CartAddProductForm()

    return render(request, 'details.html', {'item': choco_item, 'cart_form': cart_form})


def catalog_page(request):
    chocos_list = Assortment.objects.all()
    cart_form = CartAddProductForm()

    paginator = Paginator(chocos_list, 15)

    page = request.GET.get('page')
    try:
        chocos = paginator.page(page)
    except PageNotAnInteger:
        chocos = paginator.page(1)
    except EmptyPage:
        chocos = paginator.page(paginator.num_pages)

    return render(request, 'catalog.html', {'chocos': chocos, 'cart_form': cart_form})


def cart_page(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})

    return render(request, 'cart.html', {'cart': cart})


def cart_add(request, pk):
    cart = Cart(request)
    choco_item = get_object_or_404(Assortment, pk=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=choco_item, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('choco:cart')


def cart_remove(request, pk):
    cart = Cart(request)
    if request.method == 'POST':
        product = get_object_or_404(Assortment, pk = request.POST.get('itemId'))
        cart.remove(product)
        return HttpResponse(
            json.dumps({"status:":"OK"}),
            content_type="application/json"
        )

def order_page(request):
    order_form = OrderForm()
    return render(request, 'order.html', {'order_form': order_form})

def order_send(request):
    order_form = OrderForm()
    if request.method == 'POST':
        if order_form.is_valid():
            order_form.save()
            send_mail(
                'Hey there',
                'Here is the message.',
                'pauline-sh-hub@yandex.ru',
                ['pauline-sh-hub@yandex.ru'],
                fail_silently=False,
            )

    chocos_list = Assortment.objects.all()
    paginator = Paginator(chocos_list, 15)
    page = request.GET.get('page')
    try:
        chocos = paginator.page(page)
    except PageNotAnInteger:
        chocos = paginator.page(1)
    except EmptyPage:
        chocos = paginator.page(paginator.num_pages)
    return render(request, 'catalog.html', {'chocos': chocos})

def message_send(request):
    if request.method == 'POST':
        the_name = request.POST.get('the_name')
        the_email = request.POST.get('the_email')
        the_subject = request.POST.get('the_subject')
        the_message = request.POST.get('the_message')

        send_mail(
            u"ОТ: " + the_name + u" ТЕМА: " + the_subject,
            the_message,
            EMAIL_FROM,
            [the_email],
            fail_silently=False,
        )

        response_data = {}
        response_data['result'] = 'Email successful!'
        if isinstance(the_name, str):
            response_data['the_name'] = 'STR'
        elif isinstance(the_name, unicode):
            response_data['the_name'] = 'UNICODE'

        if isinstance(the_email, str):
            response_data['the_email'] = 'STR'
        elif isinstance(the_email, unicode):
            response_data['the_email'] = 'UNICODE'

        if isinstance(the_subject, str):
            response_data['the_subject'] = 'STR'
        elif isinstance(the_subject, unicode):
            response_data['the_subject'] = 'UNICODE'

        if isinstance(the_message, str):
            response_data['the_message'] = 'STR'
        elif isinstance(the_message, unicode):
            response_data['the_message'] = 'UNICODE'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
