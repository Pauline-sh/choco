# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models


class Assortment(models.Model):
    choco_name = models.CharField(max_length=100)

    choco_size = models.CharField(max_length=11)
    choco_weight = models.PositiveSmallIntegerField()
    choco_quantity_in_box = models.PositiveSmallIntegerField()

    choco_price = models.DecimalField(max_digits=10, decimal_places=2)
    choco_gt_20_price = models.DecimalField(max_digits=10, decimal_places=2)
    choco_gt_60_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    choco_pic = models.CharField(max_length=100)
    choco_art = models.CharField(max_length=100, unique=True)
    choco_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.choco_name
