# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 13:53
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogadmin', '0004_auto_20170826_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='\u6b63\u6587'),
        ),
    ]
