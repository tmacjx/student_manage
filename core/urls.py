from django.conf.urls import url, include, patterns
from . import views, ajax

urlpatterns = [
    url(r'^login/$',  views.login, name='login'),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^forget_pwd/$', views.forget_pwd, name='forget_pwd'),

    url(r'^reset_pwd/$', views.reset_pwd, name='reset_pwd'),

    url(r'^active_account/$', views.active_account, name='active_account'),

    url(r'^perfect_admin/$', views.perfect_admin, name='perfect_admin'),

    url(r'^perfect_instructor/$', views.perfect_instructor, name='perfect_instructor'),

    url(r'^perfect_student/$', views.perfect_student, name='perfect_student'),

    url(r'^show_speciality/$', views.show_speciality, name='show_speciality'),

    url(r'^show_academy/$', views.show_academy, name='show_academy'),

    url(r'^show_admin/$', views.show_admin, name='show_admin'),

    url(r'^show_group/$', views.show_group, name='show_group'),

    url(r'^show_instructor/$', views.show_instructor, name='show_instructor'),

    url(r'^show_student/$', views.show_student, name='show_student'),

    url(r'^show_thesis/$', views.show_thesis, name='show_thesis'),

    url(r'^show_thesis_self/$', views.show_thesis_self, name='show_thesis_self'),

    url(r'^show_thesis_single/$', views.show_thesis_single, name='show_thesis_single'),

    url(r'^show_papersection/$', views.show_papersection, name='show_papersection'),

    url(r'^show_papersection_single/$', views.show_papersection_single, name='show_papersection_single'),

    url(r'^show_papersection_self/$', views.show_papersection_self, name='show_papersection_self'),


]

urlpatterns += [

    url(r'^content/create_group/$', ajax.create_group),
    url(r'^content/delete_group/$', ajax.delete_group),

    url(r'^content/create_academy/$', ajax.create_academy),
    url(r'^content/delete_academy/$', ajax.delete_academy),

    url(r'^content/create_speciality/$', ajax.create_speciality),
    url(r'^content/delete_speciality/$', ajax.delete_speciality),

    url(r'^content/create_admin/$', ajax.create_admin),
    url(r'^content/delete_admin/$', ajax.delete_admin),

    url(r'^content/create_instructor/$', ajax.create_instructor),
    url(r'^content/delete_instructor/$', ajax.delete_instructor),

    url(r'^content/create_student/$', ajax.create_student),
    url(r'^content/delete_student/$', ajax.delete_student),


    url(r'^content/create_thesis/$', ajax.create_thesis),
    url(r'^content/delete_thesis/$', ajax.delete_thesis),
    url(r'^content/choice_thesis/$', ajax.choice_thesis),


    url(r'^content/login/$', ajax.login),
    url(r'^content/logout/$', ajax.logout),

    url(r'^content/create_user/$', ajax.create_user),

    url(r'^content/forget_pwd/$', ajax.forget_pwd),
    url(r'^content/reset_pwd/$', ajax.reset_pwd),
    url(r'^content/change_pwd/$', ajax.change_pwd),

    url(r'^content/perfect_admin/$', ajax.perfect_admin),

    url(r'^content/perfect_instructor/$', ajax.perfect_instructor),

    url(r'^content/perfect_student/$', ajax.perfect_student),

    url(r'^content/delete_admin/$', ajax.delete_admin),

    url(r'^content/delete_instructor/$', ajax.delete_instructor),

    url(r'^content/delete_student/$', ajax.delete_student),

    url(r'^content/get_speciality/$', ajax.get_speciality),


]