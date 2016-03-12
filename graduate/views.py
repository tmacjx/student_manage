# coding=utf-8

from django.shortcuts import render
from annoying.decorators import render_to

# Create your views here.


@render_to('graduate/login.html')
def login(request):
    pass

