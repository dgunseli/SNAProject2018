# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-05 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180404_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='satisdokumbilgi',
            name='doktor_diploma_tescil_no',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='satisdokumbilgi',
            name='firma_id',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='satisdokumbilgi',
            name='madde',
            field=models.TextField(blank=True),
        ),
    ]
