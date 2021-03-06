# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-04 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SatisDokumBilgi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eczane', models.IntegerField()),
                ('recete_no', models.TextField()),
                ('islem_tarihi', models.DateTimeField()),
                ('doktor_diploma_tescil_no', models.TextField()),
                ('verilen_adet', models.IntegerField()),
                ('urun_id', models.IntegerField()),
                ('sgketkinkod', models.TextField()),
                ('firma_id', models.IntegerField()),
                ('madde', models.TextField()),
            ],
        ),
    ]
