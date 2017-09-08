# -*- coding: utf-8 -*-
from django.conf.urls import url
from blogadmin import views

# 二级路由
urlpatterns = [
    url(r'^$', views.index, name="home_page"),
    # url(r'^index/$',views.index, name="homepage"),
    url(r'^tech/$', views.tech, name="tech_page"),
    url(r'^movie/$', views.movie, name="movie_page"),
    url(r'^movie/loadmore/', views.load_more, name="load_more"),
    url(r'^book/$', views.book, name="book_page"),
    url(r'^chat/$', views.chat, name="chat_page"),
    url(r'^tech/detail/(?P<id>\d+)/$', views.tech_detail, name="tech_detail"),
    url(r'^movie/detail/(?P<id>\d+)/$', views.movie_detail, name="movie_detail"),
    url(r'^book/detail/(?P<id>\d+)/$', views.book_detail, name="book_detail"),
    url(r'^chat/detail/(?P<id>[0-9]+)/$',views.chat_detail, name="chat_detail"),

]
