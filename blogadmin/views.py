# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from blogadmin.models import Article, FilmReview, BookReview, Essay
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from json import dumps
from datetime import date, datetime
from django.http import JsonResponse
import markdown

# 分页功能
def divide_page(request, articles):
    """
    :param request:  前端网页的url请求
    :param articles: 所有（分类）文章
    :return:   字典，分页后的文章列表和要显示的页码范围
    """
    if request.GET.get("page") == 'all':
        page = 1
        paginator = Paginator(object_list=articles, per_page=len(articles))
        articles_list = paginator.page(page)
        page_range = [1]
    else:
        before_range_num = 3         # 当前页前显示3页
        after_range_num = 2          # 当前页后显示2页，一共显示6个页码号
        list_per_page = 5            # 设置每页显示博文的数量
        try:
            # 如果请求的页码小于1或者类型错误，则默认第1页
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        # 利用django自带分页Paginator
        # 常用属性:per_page: 每页显示条目数量;  count: 数据总个数;
        # num_pages:总页数;
        # page_range:总页数的索引范围，页码的范围，从1开始，例如[1, 2, 3, 4]。
        paginator = Paginator(object_list=articles, per_page=list_per_page)
        try:
            # 取得page页码处的Page对象
            articles_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            # 如果该页不存在或者超过则跳转到尾页
            articles_list = paginator.page(paginator.num_pages)
        # print("number of pages: %s " % paginator.num_pages)
        if paginator.num_pages >= after_range_num+before_range_num+1:  # 总页数够摆满6个页码号
            # 根据当前页码号调整显示的页面范围，始终保持在前端显示6个页码号
            if page >= paginator.num_pages-after_range_num:  # 请求的页面在能显示的范围的最后6个中
                page_range = range(paginator.num_pages-before_range_num-after_range_num, paginator.num_pages+1)
            elif page >= after_range_num+before_range_num:   # 请求的页面在中间
                page_range = range(page-before_range_num, page+after_range_num+1)
            else:  #请求页面在开始的6个范围内
                page_range = range(1,7)
        else:  # 总页数不够6个
            page_range = range(1, paginator.num_pages+1)
            # 把博文列表和页码范围传参给前端模板
    return {'articles':articles_list,'page_range':page_range}


# ------  首页Homepage  index.html  --------#
def index(request):
    # get five newest blog articles: id, title, category, abstract, update_time
    articles = Article.objects.order_by('-view_times').values('id', 'title','category', 'abstract','update_time','view_times')[:5]
    # 用中文显示类别字段，手工转是因为只有all()取出来的queryset才支持get_***_display()这个自带函数
    for i in articles:
        category = i.get('category')
        #print(cat)
        if category == u'web':
            i['category'] = u'web开发'
        elif category == u'linux':
            i['category'] = u'系统运维'
        elif category == u'algorithm':
            i['category'] = u'算法'
        elif category == u'language':
            i['category'] = u'编程语言'
        else:
            i['category'] = u'其他'

    return render(request,'index.html', {"bloglist":articles},)

def tech(request):
    # 类别标签筛选器
    category_filter = request.GET.get('category','None')
    tag_filter = request.GET.get('tag','None')
    if category_filter != 'None' and tag_filter != 'None':
        tech_articles = Article.objects.filter(category=category_filter, tag=tag_filter).values('id', 'title', 'abstract', 'tag', 'update_time', 'view_times')
    elif category_filter == 'None' and tag_filter != 'None':
        tech_articles = Article.objects.filter(tag=tag_filter).values('id','title','abstract','tag','update_time','view_times')
    elif category_filter != 'None' and tag_filter == 'None':
        tech_articles = Article.objects.filter(category=category_filter).values('id', 'title', 'abstract', 'tag', 'update_time', 'view_times')
    else:
        tech_articles = Article.objects.values('id','title','abstract','tag','update_time','view_times')
    # return render(request,'tech.html', {'articles':tech_articles})
    # 先把所有数据都取出来分好页，然后根据请求的页码显示相应的数据段
    parameters_dict = divide_page(request, tech_articles)
    parameters_dict['newest_blogs'] = Article.objects.order_by('-pub_time').values('id','title')[:5]
    parameters_dict['click_rank'] = Article.objects.order_by('-view_times').values('id','title')[:5]

    return render(request, 'tech.html', parameters_dict)



def movie(request):
    newest_filmreviews = FilmReview.objects.order_by('-pub_time').values('id', 'title', 'cover','pub_time')[0:6]
    # Queryset的切片取值，从发布时间最新的开始，每次显示若干个博文
    # print("------最新的6条记录的部分索引用字段------->")
    # print(type(newest_filmreviews))
    # print newest_filmreviews
    return render(request,'movie.html',{"newest_filmreviews":newest_filmreviews})

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    """
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def queryset_to_json(querysetdata):
    """Json格式举例：
    {"bloglist": [{'id':id,'title': "文章标题",'cover':"文章封面",'pub_time': "发布时间要转成正确格式"},
            {'id':id,'title': "文章标题",'cover':"文章封面",'pub_time': "发布时间要转成正确格式"}}]}
    """
    result = {'bloglist': []}
    # print('-------- 组装成json格式----------------->')
    for i in querysetdata:
        result['bloglist'].append({'id':i.get('id',None), 'title': i.get('title','title null'), 'cover': i.get('cover','cover null'),'pub_time': dumps(i.get('pub_time',datetime.now()), default=json_serial).strip(r'"').strip().split("T")[0]})  # 时间要Json序列化后取时期格式处理 原始pub_time:""2017-08-28T17:15:27.550000+00:00""
    return JsonResponse(result)  #返回Json对象

def load_more(request):
    # data = FilmReview.objects.raw("SELECT id,title,pub_time FROM blogadmin_filmreview WHERE id=10;")[0]
    #print('----------MODELS取数据--------------->')
    # data = FilmReview.objects.values('id', 'title', 'pub_time')   # Queryset字典列表类型
    if request.method == 'POST':
        start = int(request.POST.get('offset', 0))
        size = int(request.POST.get('size', 0))
        # print("数据索引：%s %s" % (start, size))
        # 根据url的参数从数据库拉取相应的切片记录返回给ajax
        try:
            data = FilmReview.objects.order_by('-pub_time').values('id', 'title', 'cover', 'pub_time')[start:(start + size)]
            if isinstance(data, QuerySet) and data.exists():
                # print("数据合法")
                json_data = queryset_to_json(data)  # 取到了数据,转成json格式字符串或者JsonResponse对象
                # print("----- 打印后端返给ajax的数据----------->")
                # print(json_data)
                return json_data
            else:
                # raise TypeError("Type %s is not QuerySet or data from database does not exist!" % type(data))
                print("从数据库拿到数据失败！")
                return JsonResponse({'bloglist':[]})
        except Exception as err:
            print(err)
    else:  # request.method == 'GET':
        start = int(request.GET.get('offset', 0))
        size = int(request.GET.get('size', 0))
        print("数据索引：%s %s" % (start, size))
        # 根据url的参数从数据库拉取相应的切片记录返回给ajax
        try:
            data = FilmReview.objects.order_by('-pub_time').values('id', 'title', 'cover', 'pub_time')[start:(start + size)]
            if isinstance(data, QuerySet) and data.exists():
                print("数据合法")
                json_data = queryset_to_json(data)  # 取到了数据,转成json格式字符串或者JsonResponse对象
                print("----- 打印后端返给ajax的数据----------->")
                print(json_data)
                return json_data
            else:
                print("从数据库拿的数据为空！")
                return JsonResponse({'bloglist':[]})
        except Exception as err:
            print(err)


def book(request):
    book_reviews = BookReview.objects.order_by('-pub_time').values('id', 'title', 'update_time')
    return render(request,'book.html',{"book_reviews":book_reviews})

def chat(request):
    essays = Essay.objects.order_by('-pub_time').values('id', 'title', 'update_time')
    return render(request,'chat.html',{"essays":essays})
# 分类技术博文显示


# 详细博文展示
def tech_detail(request, id):
    # 根据前端请求的id获取单独的一篇文章
    try:
        article = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    # 给文章阅读量加一
    article.view_times += 1
    article.save()

    article.category = article.get_category_display()

    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.nl2br',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.extra',
                                            'markdown.extensions.headerid',
                                            'markdown.extensions.meta',
                                            'markdown.extensions.sane_lists',
                                            'markdown.extensions.tables',
                                            'markdown.extensions.toc',
                                            'markdown.extensions.wikilinks',
                                        ],)

    newest_blogs = Article.objects.order_by('-pub_time').values('id', 'title')[:5]
    click_rank = Article.objects.order_by('-view_times').values('id', 'title')[:5]
    return render(request, 'techdetail.html', context={'blog': article,'newest_blogs':newest_blogs,'click_rank':click_rank})

def movie_detail(request, id):
    # 根据前端请求的id获取单独的一篇影评
    try:
        article = FilmReview.objects.get(id=str(id))
    except FilmReview.DoesNotExist:
        raise Http404
    # 给文章阅读量加一
    article.view_times += 1
    article.save()
    return render(request, 'moviedetail.html', {'blog': article})

def book_detail(request, id):
    # 根据前端请求的id获取单独的一篇书评
    try:
        article = BookReview.objects.get(id=str(id))
    except BookReview.DoesNotExist:
        raise Http404
    # 给文章阅读量加一
    article.view_times += 1
    article.save()
    return render(request, 'bookdetail.html', {'blog': article})

def chat_detail(request, id):
    try:
        article = Essay.objects.get(id=str(id))
    except Essay.DoesNotExist:
        raise Http404
    # 给文章阅读量加一
    article.view_times += 1
    article.save()
    return render(request, 'chatdetail.html', {'blog': article})

