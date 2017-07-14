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
from django.conf.urls import url, include, patterns
from django.contrib import admin
from core import views as core_view
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^graduate/', include('graduate.urls'), name='graduate'),

    # url(r'^accounts/login/$',  core_view.login,  name='login'),
    #
    # url(r'^accounts/logout/$', core_view.logout, name='logout'),

    url(r'^account/', include('core.urls'), name='account'),

    url(r'^superadmin/$', core_view.super_admin, name='superadmin'),
    url(r'^secretary/$', core_view.admin, name='secretary'),
    url(r'^instructor/$', core_view.instructor, name='instructor'),
    url(r'^student/$', core_view.student, name='student'),


]

# urlpatterns += [
#
#     url(r'^content/index/$', ajax.index),
#     url(r'^content/login/$', core_ajax.login),
#     url(r'^content/logout/$', core_ajax.logout)
# ]

#
# if settings.DEBUG:
#     urlpatterns = patterns('',
#                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#                                {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#                            url(r'', include(
#                                'django.contrib.staticfiles.urls')),
#                            ) + urlpatterns
#

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
