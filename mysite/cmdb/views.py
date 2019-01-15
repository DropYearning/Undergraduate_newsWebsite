#  coding:utf-8
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cmdb import models


# Create your views here.
def index(request):
    # 从数据库中读出所有新闻
    news_list = models.NBAnews.objects.all()
    return_list = []
    for item in news_list:
        temp_dict = {}
        temp_dict['id'] = item.id
        temp_dict['source'] = item.source
        temp_dict['pubtime'] = item.pubtime
        temp_dict['link'] = item.link
        temp_dict['title'] = item.title
        temp_dict['keywords'] = item.keywords.split(',')
        return_list.append(temp_dict)
    
    # 分页
    paginator = Paginator(return_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "index.html", {"contacts": contacts})


def search_by_source(request, param):
    # return HttpResponse("The param is : " + param)

    # 按来源在数据库中搜索
    news_list = models.NBAnews.objects.filter(source__iexact=param)
    return_list = []
    for item in news_list:
        temp_dict = {}
        temp_dict['id'] = item.id
        temp_dict['source'] = item.source
        temp_dict['pubtime'] = item.pubtime
        temp_dict['link'] = item.link
        temp_dict['title'] = item.title
        temp_dict['keywords'] = item.keywords.split(',')
        return_list.append(temp_dict)
    # 分页
    paginator = Paginator(return_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "index.html", {"contacts": contacts})


def search_by_text(request, text):
    # 按内容在数据库中搜索
    news_list = models.NBAnews.objects.filter(content__contains=text)
    return_list = []
    for item in news_list:
        temp_dict = {}
        temp_dict['id'] = item.id
        temp_dict['source'] = item.source
        temp_dict['pubtime'] = item.pubtime
        temp_dict['link'] = item.link
        temp_dict['title'] = item.title
        temp_dict['keywords'] = item.keywords.split(',')
        return_list.append(temp_dict)
    # 分页
    paginator = Paginator(return_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "index.html", {"contacts": contacts})


def show_detail(request, param):
    # 按ID查找数据库
    news_list = models.NBAnews.objects.filter(id=param)[0]
    return render(request, "detail.html", {"news": news_list})