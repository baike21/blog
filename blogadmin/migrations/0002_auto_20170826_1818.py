# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(choices=[('Tech', '\u6280\u672f'), ('Chat', '\u6742\u6587'), ('Movie', '\u5f71\u8bc4'), ('Book', '\u8bfb\u4e66')], default='Tech', max_length=64, verbose_name='\u7c7b\u522b\u6807\u7b7e'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4'),
        ),
    ]