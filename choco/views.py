# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.validators import validate_email

from .models import Assortment
from .cart import Cart
from .forms import CartAddProductForm, OrderForm, ContactForm


EMAIL_FROM = 'pauline-sh-hub@yandex.ru'
EMAIL_TO = EMAIL_FROM


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
    chocos_list = Assortment.objects.all().order_by('id')
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
    if request.method == 'POST':
        the_name = request.POST.get('the_name')
        the_city = request.POST.get('the_city')
        the_phone_number = request.POST.get('the_phone_number')
        the_note = request.POST.get('the_note')

        response_data = {}
        try:
            cart = Cart(request)

            order_content_str = ""
            counter = 1
            for item in cart:
                product=item['product']
                order_content_str += str(counter) + ". " + product.__str__() + u"\n\t Количество: " + str(item['quantity']) + u"\n\t Цена единицы товара: " + str(item['price']) + "\n"
                counter = counter + 1
            order_content_str += u"\nОбщая стоимость заказа: " + str(cart.get_total_price())
            order_content_str += u"\nДанные заказчика: \n\tИмя: " + the_name
            order_content_str += u"\n\tТелефон:" + the_phone_number
            order_content_str += u"\n\tГород: " + the_city
            order_content_str += u"\n\tЗаметка о заказе: " + the_note

            send_mail(
                u"Новый заказ",
                order_content_str,
                EMAIL_FROM,
                [EMAIL_TO],
            )
            cart.clear()
            response_data['result'] = u'OK'
        except Exception as e:
            response_data['error'] = u'Ошибка отправки заказа. Попробуйте позже'
            response_data['result'] = u'ERROR'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def message_send(request):
    if request.method == 'POST':
        the_name = request.POST.get('the_name')
        the_email = request.POST.get('the_email')
        the_subject = request.POST.get('the_subject')
        the_message = request.POST.get('the_message')

        response_data = {}

        try:
            validate_email(the_email)
        except ValidationError:
            response_data['error'] = u'Пожалуйста, введите e-mail'
            response_data['result'] = u'ERROR'
        else:
            send_mail(
                u"ОТ: " + the_name + u" ТЕМА: " + the_subject,
                the_message,
                EMAIL_FROM,
                [the_email],
                fail_silently=False,
            )
            response_data['result'] = u'OK'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
