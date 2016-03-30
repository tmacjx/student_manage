# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from core.functions import is_super_admin, is_student, is_instructor, is_admin
from django.http.response import Http404
from annoying.decorators import render_to

# Create your views here.


@render_to('_login.html')
def login(request):
    return {}


def logout(request):
    return {}


# TODO 是否可以在login_required里面先判断是否是 superadmin
@login_required
def super_admin(request, user):
    if not is_super_admin(user):
        raise Http404
    return {}


@login_required
def admin(request):

    return {}


@login_required
def instructor(request):
    return {}


@login_required
def student(request):
    return {}





