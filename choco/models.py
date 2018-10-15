# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models


class Category (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Configuration(models.Model):
    size = models.CharField(max_length=11, blank=True)
    weight = models.PositiveSmallIntegerField(blank=True)

    stock = models.PositiveSmallIntegerField(blank=True)

    diameter = models.PositiveSmallIntegerField(blank=True)
    height = models.PositiveSmallIntegerField(blank=True)
    width = models.PositiveSmallIntegerField(blank=True)
    length = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        config_str = u"".encode("utf-8")

        if self.size:
            config_str += u"Размер упаковки: ".encode("utf-8") + self.size.encode("utf-8") + u" см; ".encode("utf-8")
        if self.weight:
            config_str += u"Вес: ".encode("utf-8") + str(self.weight).encode("utf-8") + u" г; ".encode("utf-8")
        if self.diameter:
            config_str += u"Диаметр: ".encode("utf-8") + str(self.diameter).encode("utf-8") + u" см; ".encode("utf-8")
        if self.length:
            config_str += u"Длина: ".encode("utf-8") + str(self.length).encode("utf-8") + u" см; ".encode("utf-8")
        if self.width:
            config_str += u"Ширина: ".encode("utf-8") + str(self.width).encode("utf-8") + u" см; ".encode("utf-8")
        if self.height:
            config_str += u"Высота: ".encode("utf-8") + str(self.height).encode("utf-8") + u" см; ".encode("utf-8")
        if self.stock:
            config_str += u"На складе: ".encode("utf-8") + str(self.stock).encode("utf-8") + u" шт; ".encode("utf-8")

        return config_str


class Assortment(models.Model):
    choco_name = models.CharField(max_length=100)

    choco_config = models.ManyToManyField(Configuration, blank=True)

    choco_price = models.DecimalField(max_digits=10, decimal_places=2)
    choco_gt_20_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    choco_gt_60_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    choco_pic = models.CharField(max_length=100, blank=True)
    choco_dir = models.CharField(max_length=100, blank=True)
    choco_art = models.CharField(max_length=100, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(blank=True)

    description = models.CharField(max_length=200, blank=True)

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
    client_note = models.CharField(max_length=100, blank=True)

    content = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('id',)
