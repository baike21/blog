# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-06 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogadmin', '0014_filmreview_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=b'', verbose_name='\u5c01\u9762'),
        ),
    ]