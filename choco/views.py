# -*- coding: utf-8 -*-
import json
import os

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.conf import settings
from django.forms.models import model_to_dict

from .models import Assortment, Configuration
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
    choco_configs = choco_item.choco_config.all()

    cart_form = CartAddProductForm(pk)

    if settings.DEBUG:
        static_dir = os.path.join(settings.BASE_DIR, u"choco/static/choco/choco_pics/")
    else:
        static_dir = os.path.join(settings.STATIC_ROOT, u"choco/choco_pics/")
    gallery_path = os.path.join(static_dir, choco_item.choco_dir)

    choco_gallery = []
    for f in os.listdir(gallery_path):
        if f.endswith("jpg") or f.endswith("png"): # to avoid other files
            if not f.endswith("_tn.jpg"):
                choco_gallery.append("%s%s/%s" % (u"choco/choco_pics/", choco_item.choco_dir, f))

    return render(request, 'details.html', {
        'item': choco_item,
        'configurations': choco_configs,
        'cart_form': cart_form,
        'gallery': choco_gallery
    })


def catalog_page(request):
    chocos_list = Assortment.objects.all().order_by('id')
    cart_form = CartAddProductForm(auto_id=False)

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
        item['update_quantity_form'] = CartAddProductForm(
            item['product']['id'],
            initial={
                'quantity': item['quantity'],
                'update': True,
                'configuration': item['conf_object']
            }
        )

    return render(request, 'cart.html', {'cart': cart})


def cart_add(request, choco_pk):
    cart = Cart(request)
    choco_item = get_object_or_404(Assortment, pk=choco_pk)
    config_item = Configuration.objects.filter(assortment__id=choco_pk).first()
    form = CartAddProductForm(choco_pk, request.POST, initial = {'configuration': config_item.id})
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=choco_item, configuration=config_item, quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('choco:cart')


def cart_add_conf(request, choco_pk, config_pk=-1):
    cart = Cart(request)
    choco_item = get_object_or_404(Assortment, pk=choco_pk)
    form = CartAddProductForm(choco_pk, request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if config_pk != -1:
            config_item = get_object_or_404(Configuration, pk=config_pk)
            cart.add(item=choco_item, configuration=config_item, quantity=cd['quantity'], update_quantity=cd['update'])
        else:
            cart.add(item=choco_item, configuration=cd['configuration'], quantity=cd['quantity'], update_quantity=cd['update'])

    return redirect('choco:cart')


def cart_remove(request, choco_pk, config_pk):
    cart = Cart(request)

    product = get_object_or_404(Assortment, pk=choco_pk)
    configuration = get_object_or_404(Assortment, pk=config_pk)

    cart.remove(product, configuration)

    return HttpResponse(
        json.dumps({'result': "OK", 'cart': cart.cart, 'total_items': len(cart)}),
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
                order_content_str += str(counter) + ". " + item['product']['choco_name'] + \
                                     u"\n\t Количество: " + str(item['quantity']) + \
                                     u"\n\t Конфигурация: размер: " + item['conf_object']['choco_size'] + \
                                     u" вес: " + str(item['conf_object']['choco_weight']) + u" штук в упаковке: " + str(item['conf_object']['choco_quantity_in_box']) + \
                                     u"\n\t Цена единицы товара: " + str(item['price']) + "\n"
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
            response_data['error_text'] = str(e)

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
