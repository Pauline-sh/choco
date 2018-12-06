# -*- coding: utf-8 -*-
import json
import os
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.conf import settings

from .models import Assortment, Configuration, PackageStyle
from .cart import Cart, Gift
from .forms import CartAddProductForm, OrderForm, ContactForm
from .serializers import AssortmentSerializer, PackageStyleSerializer


sale_percent = Decimal(0.9)

def get_sale_percent(request, cart):
    total_price = cart.get_total_price()
    if len(cart) > 1:
        total_price = Decimal(total_price) * Decimal(sale_percent)
    if request.session.get('cart_package', False):
        total_price = round(Decimal(total_price) + Decimal(request.session['cart_package']['package_price']), 2)
    return total_price


EMAIL_FROM = 'russian.memento@gmail.com'
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
    first_choco_config = choco_item.choco_config.first()

    cart_form = CartAddProductForm(pk)

    if settings.DEBUG:
        static_dir = os.path.join(settings.BASE_DIR, u"choco/static/choco/choco_pics/")
    else:
        static_dir = os.path.join(settings.STATIC_ROOT, u"choco/choco_pics/")
    gallery_path = os.path.join(static_dir, choco_item.choco_dir)

    choco_gallery = []
    if os.path.isdir(gallery_path):
        for f in os.listdir(gallery_path):
            if f.lower().endswith("jpg") or f.lower().endswith("png"): # to avoid other files
                if not f.lower().endswith("_tn.jpg"):
                    choco_gallery.append("%s%s/%s" % (u"choco/choco_pics/", choco_item.choco_dir, f))

    return render(request, 'details.html', {
        'item': choco_item,
        'configurations': choco_configs,
        'cart_form': cart_form,
        'gallery': choco_gallery,
        'config_types_quantity': len(choco_item.choco_config.all()),
        'first_choco_config': first_choco_config
    })


def add_catalog_pagination(request, items_list):

    paginator = Paginator(items_list, 15)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items

def catalog_choco(request):
    items_list = Assortment.objects.filter(category_id=1, available=1).order_by('id')
    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, items_list)

    return render(request, 'catalog.html', {'chocos': items, 'cart_form': cart_form})

def catalog_beresta(request):
    items_list = Assortment.objects.filter(category_id=2, available=1).order_by('id')
    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, items_list)

    return render(request, 'catalog.html', {'chocos': items, 'cart_form': cart_form})

def catalog_wood(request):
    items_list = Assortment.objects.filter(category_id=3, available=1).order_by('id')
    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, items_list)

    return render(request, 'catalog.html', {'chocos': items, 'cart_form': cart_form})


def cart_page(request):
    cart = Cart(request)
    request.session['cart_as_gift'] = False
    total_price = cart.get_total_price()
    package_styles = PackageStyle.objects.all()
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price, 'package_styles':package_styles})


def cart_as_gift_total_price(request, cart):
    total_price = cart.get_total_price()
    if request.session['cart_as_gift']:
        return get_sale_percent(request, cart) # round(Decimal(total_price) * sale_percent + Decimal(request.session['cart_package']['package_price']), 2)
    return total_price


def cart_add(request, choco_pk):
    cart = Cart(request)
    if request.method == 'POST':
        choco_item = get_object_or_404(Assortment, pk=choco_pk)
        if(int(request.POST.get("configId")) == -1):
            config_item = Configuration.objects.filter(assortment__id=choco_pk).first()
        else:
            config_item = get_object_or_404(Configuration, pk=request.POST.get("configId"))
        new_item = cart.add(
            item=choco_item,
            configuration=config_item,
            quantity=int(request.POST.get('newValue')),
            update_quantity=False
        )

        static_dir = u"/static/choco/choco_pics/"

        return HttpResponse(
            json.dumps({'result': "OK", 'cart': cart.cart, 'total_items': len(cart), "new_item": new_item, "static_dir": static_dir}),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps({'result': "OK", 'cart': cart.cart, 'total_items': len(cart)}),
        content_type="application/json"
    )

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
    total_cart_price = round(cart.get_total_price(), 2)
    if request.method == 'POST':
        product = get_object_or_404(Assortment, pk=choco_pk)
        configuration = get_object_or_404(Configuration, pk=config_pk)
        cart.remove(product, configuration)

        total_cart_price = round(cart.get_total_price(), 2)
        if request.session.get('cart_as_gift', False):
            total_cart_price = cart_as_gift_total_price(request, cart)

    return HttpResponse(
        json.dumps({'result': "OK", 'cart': cart.cart, 'total_items': len(cart), 'total_cart_price': total_cart_price}),
        content_type="application/json"
    )

def cart_update(request, choco_pk, config_pk):
    cart = Cart(request)
    total_price = 0
    total_cart_price = cart.get_total_price()
    if request.method == 'POST':
        product = get_object_or_404(Assortment, pk=choco_pk)
        configuration = get_object_or_404(Configuration, pk=config_pk)
        cart.add(
            item=product,
            configuration=configuration,
            quantity=int(request.POST.get('newValue')),
            update_quantity=True
        )
        for config in cart.cart[str(choco_pk)]:
            if config['configuration'] == config_pk:
                total_price = str(Decimal(config['price']) * config['quantity'])
                break

        total_cart_price = cart.get_total_price()
        if request.session.get('cart_as_gift', False):
            total_cart_price = cart_as_gift_total_price(request, cart)

    return HttpResponse(
        json.dumps({'result': "OK",
                    'cart': cart.cart,
                    'total_items': len(cart),
                    'total_price': total_price,
                    'total_cart_price': total_cart_price,
                    }),
        content_type="application/json"
    )

def cart_as_gift(request):
    cart = Cart(request)
    total_price = cart.get_total_price()
    if request.method == 'POST':
        request.session['cart_as_gift'] = False
        request.session['cart_package'] = False
    return HttpResponse(
        json.dumps({'result': "OK", 'cart': cart.cart, 'total_items': len(cart), 'total_price': total_price}),
        content_type="application/json"
    )

def cart_as_gift_package(request, package_pk):
    cart = Cart(request)
    total_price = cart.get_total_price()
    if request.method == 'POST':
        gift_switch = request.POST.get('gift_switch')
        if gift_switch == "true":
            request.session['cart_as_gift'] = True
            package_query = PackageStyle.objects.get(pk=package_pk)
            request.session['cart_package'] = PackageStyleSerializer(package_query).data
            total_price = cart_as_gift_total_price(request, cart)
        else:
            request.session['cart_as_gift'] = False
            request.session['cart_package'] = False
    return HttpResponse(
        json.dumps({'result': "OK", 'cart': cart.cart, 'total_items': len(cart), 'total_price': total_price}),
        content_type="application/json"
    )


def gift_page(request):
    gift = Gift(request)
    package_styles = PackageStyle.objects.all()
    total_price = gift.get_total_price()
    gift_len = len(gift)

    if gift.get_package():
        gift_package_id = int(gift.get_package()['id'])
    else:
        gift_package_id = -1

    return render(request, 'gift.html', {
        'package_styles': package_styles,
        'total_price': total_price,
        'sale_percent': sale_percent,
        'gift_len': gift_len,
        'gift_package_id': gift_package_id,
    })

def gift_add(request, choco_pk):
    gift = Gift(request)
    if request.method == 'POST':
        choco_item = get_object_or_404(Assortment, pk=choco_pk)
        if(int(request.POST.get("configId")) == -1):
            config_item = Configuration.objects.filter(assortment__id=choco_pk).first()
        else:
            config_item = get_object_or_404(Configuration, pk=request.POST.get("configId"))
        new_item = gift.add(
            item=choco_item,
            configuration=config_item,
            quantity=int(request.POST.get('newValue')),
            update_quantity=False
        )
        package = gift.get_package()
        total_price = gift.get_total_price()
        static_dir = u"/static/choco/choco_pics/"

        return HttpResponse(
            json.dumps({
                'result': "OK",
                'gift': gift.cart,
                'total_items': len(gift),
                "total_price": total_price,
                "new_item": new_item,
                "static_dir": static_dir,
                'package':package
            }),
            content_type="application/json"
        )
    return HttpResponse(
        json.dumps({'result': "OK", 'gift': gift.cart, 'total_items': len(gift)}),
        content_type="application/json"
    )

def gift_remove(request, choco_pk, config_pk):
    gift = Gift(request)
    if request.method == 'POST':
        product = get_object_or_404(Assortment, pk=choco_pk)
        configuration = get_object_or_404(Configuration, pk=config_pk)
        gift.remove(product, configuration)

    package = gift.get_package()
    total_price = gift.get_total_price()

    return HttpResponse(
        json.dumps({'result': "OK", 'gift': gift.cart, 'total_items': len(gift), "total_price": total_price, 'package': package}),
        content_type="application/json"
    )

def gift_get_items(request, category_pk):
    if request.method == 'POST':
        items_list = Assortment.objects.filter(category_id=category_pk, available=1).order_by('id')
        items = []
        for item in items_list:
            items.append(AssortmentSerializer(item).data)

        return HttpResponse(
            json.dumps(items),
            content_type="application/json"
        )
    return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
        content_type="application/json"
    )

def gift_state(request):
    if request.method == 'POST':
        gift = Gift(request)
        if len(gift) == 0:
            return HttpResponse(
                json.dumps({'result': 'NOT OK', 'error': 'Нет выбранных товаров!'}),
                content_type="application/json"
            )
        request.session['gift_state'] = True
        gift.set_package(request.POST.get("packageValue"))
        return HttpResponse(
            json.dumps({'result': 'OK'}),
            content_type="application/json"
        )
    return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
        content_type="application/json"
    )

def gift_get_total_price(request, package_pk):
    if request.method == 'POST':
        gift = Gift(request)
        gift.set_package(package_pk)
        total_price = gift.get_total_price()
        package = gift.get_package()
        return HttpResponse(
            json.dumps({'result': 'OK', 'total_price': total_price, 'package': package}),
            content_type="application/json"
        )
    return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
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
            order_content_str = ""
            counter = 1
            if not request.session.get('gift_state', False):
                cart = Cart(request)
                if request.session.get('cart_as_gift', False) and request.session.get('cart_package', False):
                    if len(cart) < 2:
                        sale_percent = 1
                    for item in cart:
                        configuration = Configuration.objects.get(pk=item['configuration'])
                        order_content_str += str(counter) + u". " + item['product']['choco_name'] + \
                                             u"\n\t Количество товаров: " + str(item['quantity']) + \
                                             u"\n\t Конфигурация: " + configuration.__str__().decode('utf-8') + \
                                             u"\n\t Цена единицы товара: " + str(round(Decimal(item['price']) * sale_percent, 2)) + "\n"
                        counter = counter + 1
                    packageStyle = request.session['cart_package']
                    order_content_str += u"\nВыбранная упаковка и ее цена: " + packageStyle['package_name'] + u" " + str(packageStyle['package_price'])
                    total_price = get_sale_percent(request, cart)
                    order_content_str += u"\nОбщая стоимость заказа: " + str(total_price)

                    request.session['cart_as_gift'] = False
                    request.session['cart_package'] = False
                else:
                    for item in cart:
                        configuration = Configuration.objects.get(pk=item['configuration'])
                        order_content_str += str(counter) + u". " + item['product']['choco_name'] + \
                                             u"\n\t Количество товаров: " + str(item['quantity']) + \
                                             u"\n\t Конфигурация: " + configuration.__str__().decode('utf-8') + \
                                             u"\n\t Цена единицы товара: " + str(item['price']) + "\n"
                        counter = counter + 1
                    order_content_str += u"\nОбщая стоимость заказа: " + str(cart.get_total_price())
            else:
                cart = Gift(request)
                if len(cart) < 2:
                    sale_percent = 1
                for item in cart:
                    configuration = Configuration.objects.get(pk=item['configuration'])
                    order_content_str += str(counter) + u". " + item['product']['choco_name'] + \
                                         u"\n\t Количество товаров: " + str(item['quantity']) + \
                                         u"\n\t Конфигурация: " + configuration.__str__().decode('utf-8') + \
                                         u"\n\t Цена единицы товара: " + str(round(Decimal(item['price']) * sale_percent, 2)) + "\n"
                    counter = counter + 1
                order_content_str += u"\nОбщая стоимость заказа: " + str(cart.get_total_price())
                order_content_str += u"\nВыбранная упаковка и ее цена: " + cart.package['package_name'] + u" " + str(cart.package['package_price'])
                request.session['gift_state'] = False

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
                u"e-mail отправителя: " + the_email + "\n" + the_message,
                EMAIL_FROM,
                [EMAIL_TO],
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
