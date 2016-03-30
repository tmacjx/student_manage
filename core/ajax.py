# coding=utf-8
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from util.functions import json_response
from core.functions import check_user


@require_POST
def login(request):
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    if not AuthenticationForm():
        result['msg'] = u'验证失败'
        return json_response(result)
    # check_user(use)
    user = authenticate(request, request.POST)
    if user is not None:
        if not check_user(user):
            result['msg'] = u'验证失败,请选择正确的登录类型'
            return json_response(result)
    auth_login(request, user)
    if not user.is_active:
        user.is_active = 1
    result['status'] = 1
    result['msg'] = u'登录成功'
    # TODO 根据登录的类型来进行相应的跳转  不通过url,通过调用视图来进行跳转super_admin(request, user):
    return json_response(result)


@require_POST
def logout(request):
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    user = request.user
    auth_logout(request, user)
    result['status'] = 1
    result['msg'] = u'登出成功'
    return json_response(result)


@require_POST
def add_student():
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}


@require_POST
def add_instructor():
    pass


@require_POST
def add_admin():
    pass