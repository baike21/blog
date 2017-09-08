# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blogadmin.models import Article,FilmReview,BookReview,Essay
# from django.db import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'tag', 'pub_time', 'update_time','view_times')
    list_editable = ('category',)
    list_filter = ('category', 'tag')
    list_per_page = 8


class FilmReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'pub_time', 'update_time','view_times')
    list_editable = ('tag',)
    list_filter = ('tag',)
    list_per_page = 8


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'pub_time', 'update_time','view_times')
    list_editable = ('tag',)  # 注意list_display第一项不能被编辑
    list_filter = ('tag',)
    list_per_page = 8


class EssayAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'pub_time', 'update_time','view_times')
    list_editable = ('tag',)
    list_filter = ('tag',)
    list_per_page = 8


# Register your models here.
admin.site.register(Article,ArticleAdmin)
admin.site.register(FilmReview,FilmReviewAdmin)
admin.site.register(BookReview,BookReviewAdmin)
admin.site.register(Essay,EssayAdmin)
