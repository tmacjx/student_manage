"""student_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from student_manage import ajax
from core import views as core_view
from core import ajax  as core_ajax

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^graduate/', include('graduate.urls'), name='graduate'),

    url(r'^accounts/login/$',  core_view.login,  name='login'),

    url(r'^accounts/logout/$', core_view.logout, name='logout'),


]

urlpatterns += [

    url(r'^content/index/$', ajax.index),
    url(r'^content/login/$', core_ajax.login),
    url(r'^content/logout/$', core_ajax.logout),


]