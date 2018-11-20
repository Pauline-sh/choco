# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-20 07:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assortment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choco_name', models.CharField(max_length=100)),
                ('choco_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('choco_gt_20_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('choco_gt_60_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('choco_pic', models.CharField(blank=True, max_length=100)),
                ('choco_dir', models.CharField(blank=True, max_length=100)),
                ('choco_art', models.CharField(blank=True, max_length=100)),
                ('available', models.BooleanField()),
                ('description', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=20)),
                ('weight', models.PositiveSmallIntegerField(blank=True)),
                ('stock', models.PositiveSmallIntegerField(blank=True)),
                ('diameter', models.PositiveSmallIntegerField(blank=True)),
                ('height', models.PositiveSmallIntegerField(blank=True)),
                ('width', models.PositiveSmallIntegerField(blank=True)),
                ('length', models.PositiveSmallIntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100)),
                ('client_city', models.CharField(max_length=100)),
                ('client_phone', models.CharField(max_length=20)),
                ('client_note', models.CharField(blank=True, max_length=100)),
                ('content', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PackageStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=30)),
                ('package_pic', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='assortment',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choco.Category'),
        ),
        migrations.AddField(
            model_name='assortment',
            name='choco_config',
            field=models.ManyToManyField(blank=True, to='choco.Configuration'),
        ),
    ]
