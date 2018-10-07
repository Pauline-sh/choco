# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models


class Configuration(models.Model):
    choco_size = models.CharField(max_length=11)
    choco_weight = models.PositiveSmallIntegerField()
    choco_quantity_in_box = models.PositiveSmallIntegerField()

    def __str__(self):
        return u"Размер упаковки: ".encode("utf-8") + self.choco_size.encode("utf-8") + \
               u"; Вес: ".encode("utf-8") + str(self.choco_weight).encode("utf-8") + \
               u"; Шт. в упаковке: ".encode("utf-8") + str(self.choco_quantity_in_box).encode("utf-8")


class Assortment(models.Model):
    choco_name = models.CharField(max_length=100)

    choco_config = models.ManyToManyField(Configuration)

    choco_price = models.DecimalField(max_digits=10, decimal_places=2)
    choco_gt_20_price = models.DecimalField(max_digits=10, decimal_places=2)
    choco_gt_60_price = models.DecimalField(max_digits=10, decimal_places=2)

    choco_pic = models.CharField(max_length=100)
    choco_dir = models.CharField(max_length=100)
    choco_art = models.CharField(max_length=100)
    choco_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.choco_name

    class Meta:
        ordering = ('id',)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('choco:details', args=[str(self.id)])


class Orders(models.Model):
    client_name = models.CharField(max_length=100)
    client_city = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20)
    client_note = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_conf = models.CharField(max_length=100)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('id',)
