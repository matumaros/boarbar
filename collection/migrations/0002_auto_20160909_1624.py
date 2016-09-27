# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-09 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionitem',
            name='kind',
            field=models.CharField(choices=[('tongue_twister', 'zunga breha'), ('saying', 'šbruh'), ('song', 'liad'), ('poem', 'gedihd')], max_length=50),
        ),
    ]
