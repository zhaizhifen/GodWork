# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from controller.public.pagination import Paginator_ajax
from controller.core.public import *
from models import *
from User.forms import *
from GodWork.views import hashpassword
from django.http import HttpResponse
import json

# Create your views here.


def index(request):
    # 用户列表
    statue = "用户列表"
    users = User.objects.all()
    return render_to_response('user/index.html', locals(), context_instance=RequestContext(request))


def edit(request, id):
    # 编辑
    statue = "编辑"
    user = User.objects.get(pk=id)
    if request.method == "POST" and request.POST:
        registerFrom = RegisterForm(request.POST, request.FILES)
        # print(registerFrom.is_valid())
        if registerFrom.is_valid():
            clear_data = registerFrom.cleaned_data
            user.username = clear_data.get('username')
            user.password = hashpassword(clear_data.get("password"))
            user.email = clear_data.get("email")
            user.phone = clear_data.get("phone")
            user.save()
            # print request.POST.get('username'), clear_data.get("email")
            # print user.username, user.password, user.photo, user.email, user.phone
            return HttpResponseRedirect("/user/index/")
    else:
        registerFrom = RegisterForm()
    return render_to_response('user/edit.html', locals(), context_instance=RequestContext(request))


def delete(request, id):
    # 删除
    statue = "删除"
    User.objects.get(pk=id).delete()
    users = User.objects.all()
    return render_to_response('user/index.html', locals(), context_instance=RequestContext(request))


def GetDepartment(request):
    response = HttpResponse()
    currency = Currency(request)
    rq_get = getattr(currency, 'rq_get')
    page_num = int(rq_get('offset'))
    PAGE_SIZE = int(rq_get('limit'))
    users = User.objects.all().values()
    pager = Paginator_ajax(page_num, users, PAGE_SIZE)

    response.write(json.dumps(pager.data))
    return response


def uedit(request):
    response = HttpResponse()
    currency = Currency(request)
    rq_get = getattr(currency, 'rq_get')
    username = rq_get('username')
    email = rq_get('email')
    phone = rq_get('phone')
    id = rq_get('id')
    user = User.objects.get(pk=id)
    user.username = username
    user.email = email
    user.phone = phone
    user.save()
    response.write(json.dumps('123'))
    return response