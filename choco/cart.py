# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from .models import Assortment


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, configuration, quantity=1, update_quantity=False):
        item_id = str(item.id)
        if configuration != None:
            config_id = str(configuration.id)

            # если такого продукта вообще не было в корзине
            if item_id not in self.cart:
                self.cart[item_id] = [{
                    'configuration': config_id,
                    'quantity': 0,
                    'price': str(item.choco_price)
                }]

            # если такой продукт был но в другой конфигурации
            elif not any(item_config['configuration'] == config_id for item_config in self.cart[item_id]):
                self.cart[item_id].append({
                    'configuration': config_id,
                    'quantity': 0,
                    'price': str(item.choco_price)
                })

            if update_quantity:
                for item_config in self.cart[item_id]:
                    if(item_config['configuration'] == config_id):
                        item_config['quantity'] = quantity
            else:
                for item_config in self.cart[item_id]:
                    if(item_config['configuration'] == config_id):
                        item_config['quantity'] += quantity

            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, item, configuration):
        item_id = str(item.id)
        config_id = str(configuration.id)
        if item_id in self.cart:
            for item_config in list(self.cart[item_id]):
                if(item_config['configuration'] == config_id):
                    self.cart[item_id].remove(item_config)
                    if(len(self.cart[item_id]) == 0):
                        del self.cart[item_id]
                    self.save()
                    return


    def __iter__(self):
        item_ids = self.cart.keys()
        items = Assortment.objects.filter(id__in=item_ids)
        for item in items:
            conf_objects = item.choco_config.all()
            for conf_object in conf_objects:
                for config in self.cart[str(item.id)]:
                    if config['configuration'] == str(conf_object.id):
                        config['conf_object'] = conf_object
                        config['product'] = item

        for item in self.cart.values():
            for config in item:
                config['price'] = Decimal(config['price'])
                config['total_price'] = config['price'] * config['quantity']
                yield config

    def __len__(self):
        sum = 0
        for item in self.cart.values():
            for config in item:
                sum += config['quantity']
        return sum

    def get_total_price(self):
        sum = 0
        for item in self.cart.values():
            for config in item:
                sum += Decimal(config['price']) * config['quantity']
        return sum

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
