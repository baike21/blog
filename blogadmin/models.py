# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from DjangoUeditor.models import UEditorField


IT_CATEGORY_CHOICES = (
    ('web',u'Web开发'),
    ('linux',u'系统运维'),
    ('algorithm',u'算法'),
    ('language',u'编程语言'),
    ('others',u'其他'),
)

# 技术类博客文章,默认用markdown编辑器
class Article(models.Model):
    title = models.CharField(u'标题', max_length=128, blank=True, null=True)
    category = models.CharField(u'类别', max_length=64, choices=IT_CATEGORY_CHOICES, default='web')
    tag = models.CharField(u'标签', max_length=16, blank=True, null=True)
    abstract = models.TextField(u'摘要', blank=True, null=True)
    pub_time = models.DateTimeField(u'发布时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    content = models.TextField(u'正文', blank=True, null=True)
    #content = UEditorField(u'正文', height=300, width=1000, default=u'', blank=True, imagePath='uploads/blog/images/', toolbars='besttome', filePath='uploads/blog/files/')
    view_times = models.IntegerField(u'阅读量', default=0)

    def __unicode__(self):
        # return self.title
        return "{'title': %s, 'pub_time': %s}" % (self.title, self.pub_time.strftime("%Y-%m-%d"))

    class Meta:  # 按更新时间降序排列
        ordering = ['-update_time']
        verbose_name = u'技术类博客'
        verbose_name_plural = u'技术类博客'


# 影视评论类博客文章，默认用ueditor编辑器
class FilmReview(models.Model):
    title = models.CharField(u'标题', max_length=128, blank=True, null=True)
    cover = models.ImageField(u'封面', blank=True, null=True)
    tag = models.CharField(u'标签', max_length=16, blank=True, null=True)
    pub_time = models.DateTimeField(u'发布时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    content = UEditorField(u'正文', height=300, width=1000, default=u'', blank=True, imagePath='uploads/blog/images/',
                           toolbars='besttome', filePath='uploads/blog/files/')
    view_times = models.IntegerField(u'阅读量', default=0)

    def __unicode__(self):
        # return self.title
        return "{'title': %s, 'pub_time': %s}" % (self.title,self.pub_time.strftime("%Y-%m-%d"))

    class Meta:  # 按发表时间降序排列
        ordering = ['-pub_time']
        verbose_name = u'影视评论'
        verbose_name_plural = u'影视评论'

# 书籍评论类博客文章
class BookReview(models.Model):
        title = models.CharField(u'标题', max_length=128, blank=True, null=True)
        cover = models.ImageField(u'封面', blank=True, null=True)
        tag = models.CharField(u'标签', max_length=16, blank=True, null=True)
        pub_time = models.DateTimeField(u'发布时间', auto_now_add=True)
        update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
        content = UEditorField(u'正文', height=300, width=1000, default=u'', blank=True, imagePath='uploads/blog/images/',
                               toolbars='besttome', filePath='uploads/blog/files/')
        view_times = models.IntegerField(u'阅读量', default=0)

        def __unicode__(self):
            return "{'title': %s, 'pub_time': %s}" % (self.title, self.pub_time.strftime("%Y-%m-%d"))

        class Meta:  # 按发表时间降序排列
            ordering = ['-pub_time']
            verbose_name = u'书刊评论'
            verbose_name_plural = u'书刊评论'

# 杂文
class Essay(models.Model):
    title = models.CharField(u'标题', max_length=128, blank=True, null=True)
    tag = models.CharField(u'标签', max_length=16, blank=True, null=True)
    pub_time = models.DateTimeField(u'发布时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    content = UEditorField(u'正文', height=300, width=1000, default=u'', blank=True, imagePath='uploads/blog/images/',toolbars='besttome', filePath='uploads/blog/files/')
    view_times = models.IntegerField(u'阅读量', default=0)

    def __unicode__(self):
        return "{'title': %s, 'pub_time': %s}" % (self.title, self.pub_time.strftime("%Y-%m-%d"))

    class Meta:  # 按发表时间降序排列
        ordering = ['-pub_time']
        verbose_name = u'杂文'
        verbose_name_plural = u'杂文'

# 评论(现只针对技术博文)
class Comment(models.Model):
    flag = models.ForeignKey(Article)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL)
    publish_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    content = models.TextField()
    root_id = models.IntegerField(default=0)  # 评论的最上层评论，若该评论处于最上层，则为0，
    parent_id = models.IntegerField(default=0)  # 评论的父评论，若无父评论，则为0

    def __unicode__(self):
        return self.content



