from django.conf.urls import url, include
from graduate import views
from graduate import ajax

urlpatterns = [
    url(r'^login/$', views.login),




]

urlpatterns += [

    url(r'^content/login/$', ajax.login),


]