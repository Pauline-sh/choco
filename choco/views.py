# -*- coding: utf-8 -*-
import json
import os
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.db.models import Q

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
EMAIL_TO = 'chocosuvenir@yandex.ru'

#1-2-7 = old version
#1-2-8 = new version
URL_OLD = 'memento'

def home_page(request):
    contact_form = ContactForm()
    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True
    return render(request, 'home.html', {'contact_form': contact_form, 'redesign': redesign, 'url': request.build_absolute_uri()})


def about_page(request):
    contact_form = ContactForm()
    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True
    return render(request, 'about.html', {'contact_form': contact_form, 'redesign': redesign})


def contacts_page(request):
    contact_form = ContactForm()
    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True
    return render(request, 'contacts.html', {'contact_form': contact_form, 'redesign': redesign})


def details_page(request, pk):
    contact_form = ContactForm()

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

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'details.html', {
        'item': choco_item,
        'configurations': choco_configs,
        'cart_form': cart_form,
        'gallery': choco_gallery,
        'config_types_quantity': len(choco_item.choco_config.all()),
        'first_choco_config': first_choco_config,
        'contact_form': contact_form,
        'redesign': redesign
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
    contact_form = ContactForm()

    items_list = Assortment.objects.filter(category_id=1, available=1).order_by('id')
    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, items_list)

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'catalog.html', {'chocos': items, 'cart_form': cart_form, 'contact_form': contact_form, 'redesign': redesign})

def catalog_beresta(request, subcategory_pk):
    contact_form = ContactForm()

    items_list = Assortment.objects.filter(category_id=2, subcategory_id=subcategory_pk, available=1).order_by('id')
    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, items_list)

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'catalog.html', {'chocos': items, 'cart_form': cart_form, 'contact_form': contact_form, 'redesign': redesign})

def catalog_wood(request):
    contact_form = ContactForm()

    items_list = Assortment.objects.filter(category_id=3, available=1).order_by('-id')
    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, items_list)

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'catalog.html', {'chocos': items, 'cart_form': cart_form, 'contact_form': contact_form, 'redesign': redesign})


def cart_page(request):
    contact_form = ContactForm()

    cart = Cart(request)
    request.session['cart_as_gift'] = False
    total_price = cart.get_total_price()
    package_styles = PackageStyle.objects.all()

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price, 'package_styles':package_styles, 'contact_form': contact_form, 'redesign': redesign})


def cart_as_gift_total_price(request, cart):
    total_price = cart.get_total_price()
    if request.session['cart_as_gift']:
        return get_sale_percent(request, cart)
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
    contact_form = ContactForm()

    gift = Gift(request)
    package_styles = PackageStyle.objects.all()
    total_price = gift.get_total_price()

    if gift.get_package():
        gift_package_id = int(gift.get_package()['id'])
    else:
        gift_package_id = -1

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'gift.html', {
        'package_styles': package_styles,
        'total_price': total_price,
        'sale_percent': sale_percent,
        'gift_len': len(gift),
        'gift_package_id': gift_package_id,
        'contact_form': contact_form,
        'redesign': redesign
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

def gift_get_items(request, category_pk, subcategory_pk):
    if request.method == 'POST':
        items_list = Assortment.objects.filter(category_id=category_pk, subcategory_id=subcategory_pk, available=1).order_by('id')
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
    contact_form = ContactForm()

    order_form = OrderForm()

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'order.html', {
        'order_form': order_form,
        'contact_form': contact_form,
        'redesign': redesign
    })

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
                        sale_percent = Decimal(1)
                    else:
                        sale_percent = Decimal(0.9)
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
                    sale_percent = Decimal(1)
                else:
                    sale_percent = Decimal(0.9)
                for item in cart:
                    configuration = Configuration.objects.get(pk=item['configuration'])
                    item_price = str(round(Decimal(item['price']) * sale_percent, 2))
                    order_content_str += u"Подарочный набор\n"
                    order_content_str += str(counter) + u". " + item['product']['choco_name'] + \
                                         u"\n\t Количество товаров: " + str(item['quantity']) + \
                                         u"\n\t Конфигурация: " + configuration.__str__().decode('utf-8') + \
                                         u"\n\t Цена единицы товара: " + item_price + "\n"
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
        the_phone = request.POST.get('the_phone')

        response_data = {}

        send_mail(
            u"Заказ звонка",
            u"Заказ звонка от: " + the_name + u" Номер телефона: " + the_phone,
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

def search_page(request):
    contact_form = ContactForm()

    query = request.GET.get('query')
    querylist = query.split()
    response = Assortment.objects.filter(reduce(lambda x, y: x | y, [(Q(choco_name__icontains=word) | Q(description__icontains=word)) for word in querylist])).filter(available=1)
    result = []

    for item in response:
        result.append(AssortmentSerializer(item).data)

    result.sort(
        key = lambda item: get_keyword_matches(item['choco_name'], querylist), reverse=True
    )

    result = result[0:100]

    cart_form = CartAddProductForm(auto_id=False)
    items = add_catalog_pagination(request, result)    

    if URL_OLD in request.build_absolute_uri():
        redesign = False
    else:
        redesign = True

    return render(request, 'search.html', {'chocos': items, 'cart_form': cart_form, 'contact_form': contact_form, 'query': query, 'redesign': redesign})

def quick_search(request):
    if request.method == 'GET':
        querylist = request.GET.get('query').split()
        response = Assortment.objects.filter(reduce(lambda x, y: x | y, [(Q(choco_name__icontains=word) | Q(description__icontains=word)) for word in querylist])).filter(available=1)
        result = []

        for item in response:
            result.append(AssortmentSerializer(item).data)

        result.sort(
            key = lambda item: get_keyword_matches(item['choco_name'], querylist), reverse=True
        )

        return HttpResponse(
            json.dumps({'result': "OK", 'data': result[0:3]}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def get_keyword_matches(name, keywords):
    count = 0

    for word in keywords:
        if word.lower() in name.lower():
            count = count + 1

    return count

def verify(request, file):
    return FileResponse(open(os.path.join(settings.BASE_DIR, u"choco/" + file)))