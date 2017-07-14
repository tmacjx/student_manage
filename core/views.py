# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from core.functions import is_super_admin, is_student, is_instructor, is_admin, get_user_admin, get_user_instructor,\
                           get_user_student
from django.http.response import Http404, HttpResponseRedirect
from annoying.decorators import render_to
from django.views.decorators.http import require_GET, require_POST
from core.models import VerityCode, VerityCodeType
from django.contrib.auth import authenticate
from django.db import transaction
from django.utils import timezone
from core.forms import SuperAdminForm, AdminForm, StudentForm, InstructorForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
from core.models import Academy, Speciality, Student, Instructor, Admin, SuperAdmin, Thesis, PaperSection
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse


# Create your views here.


@render_to('_login.html')
def login(request):
    return {}


def logout(request):
    return {}


# TODO 是否可以在login_required里面先判断是否是 superadmin
@login_required
@render_to('_superadmin.html')
def super_admin(request):
    user = request.user
    if not is_super_admin(user):
        raise Http404
    return HttpResponseRedirect(reverse('show_group'))


@login_required
@render_to('_admin.html')
def admin(request):
    user = request.user
    if not is_admin(user):
        raise Http404
    # admin = get_user_admin(user)
    # academy = admin.academy
    # return HttpResponseRedirect(reverse('show_instructor', key=academy))
    return HttpResponseRedirect(reverse('show_instructor'))


@login_required
@render_to('_instructor.html')
def instructor(request):
    user = request.user
    if not is_instructor(user):
        raise Http404
    return HttpResponseRedirect(reverse('show_thesis_self'))


@login_required
@render_to('_student.html')
def student(request):
    user = request.user
    if not is_student(user):
        raise Http404
    return HttpResponseRedirect(reverse('show_thesis_single'))


# 激活码 激活 忘记 重置

@render_to('core/forget_pwd.html')
def forget_pwd(request):
    return {}


@render_to('core/reset_pwd.html')
def reset_pwd(request):
    verify_code = request.GET.get('code', '')
    try:
        vcode = VerityCode.objects.get(code=verify_code, code_type=VerityCodeType.FORGET_PWD)
    except VerityCode.DoesNotExist:
        raise Http404
    if vcode.is_used or timezone.now() > vcode.expire_time:
        raise Http404
    user = authenticate(remote_user=vcode.user)
    with transaction.atomic():
        vcode.is_used = True
        vcode.save()
        auth_login(request, user)
    return {}


def change_pwd(request):
    return {}


@require_GET
@render_to('core/active_account.html')
def active_account(request):
    # 根据不同的用户分配不同的权限
    # TODO 激活页面要求根据user的类型 提供不同的表单, 进行完善信息, 完善后, 进入跳转
    verify_code = request.GET.get('code', '')
    try:
        vcode = VerityCode.objects.get(code=verify_code, code_type=VerityCodeType.ACTIVE_ACCOUNT)
    except VerityCode.DoesNotExist:
        raise Http404
    if vcode.is_used or timezone.now() > vcode.expire_time:
        raise Http404
    user = authenticate(remote_user=vcode.user)
    with transaction.atomic():
        vcode.is_used = True
        vcode.save()
        user.is_active = True
        user.email = vcode.email
        user.save()
        auth_login(request, user)
    # # TODO 跳转到login页面
    return {}


@require_GET
@render_to('core/edit_admin.html')
@login_required
# TODO 权限检查必须是管理员
def perfect_admin(request):
    user = request.user
    admin_match = get_user_admin(user)
    if not admin_match:
        raise Http404
    system_info = admin_match.academy.name
    academy_all = Academy.objects.filter()
    return {'admin': admin_match, 'system_info': system_info, 'academy_all': academy_all}


@require_GET
@render_to('core/edit_instructor.html')
@login_required
def perfect_instructor(request):
    user = request.user
    instructor_match = get_user_instructor(user)
    if not instructor_match:
        raise Http404
    system_info = instructor_match.academy.name
    academy_all = Academy.objects.filter()
    return {'instructor': instructor_match, 'system_info': system_info, 'academy_all': academy_all}


@require_GET
@render_to('core/edit_student.html')
@login_required
def perfect_student(request):
    user = request.user
    student_match = get_user_student(user)
    if not student_match:
        raise Http404
    system_info = student_match.academy.name
    academy_all = Academy.objects.filter()
    return {'student': student_match, 'system_info': system_info, 'academy_all': academy_all}


@require_GET
@render_to('core/show_speciality.html')
def show_speciality(request):
    """
    超级管理员 配置专业页面
    :param request:
    :return:
    """
    user = request.user
    if not user.is_superuser:
        raise Http404
    speciality_all = Speciality.objects.all()
    academy_all = Academy.objects.all()
    paginator = Paginator(speciality_all, 10)
    page_num = request.GET.get('page')
    try:
        speciality_all = paginator.page(page_num)
    except PageNotAnInteger:
        speciality_all = paginator.page(1)
    except EmptyPage:
        speciality_all = paginator.page(paginator.num_pages)
    system_info = '超级管理员'
    return {'speciality_all': speciality_all, 'academy_all': academy_all, 'system_info': system_info, 'user': user}


@require_GET
@render_to('core/show_admin.html')
def show_admin(request):
    """
    超级管理员 配置管理员页面
    :param request:
    :return:
    """
    user = request.user
    if not user.is_superuser:
        raise Http404
    academy_all = Academy.objects.all()
    admin_all = Admin.objects.all()
    system_info = "超级管理员"
    return {'academy_all': academy_all, 'admin_all': admin_all, 'system_info': system_info, 'user': user}


@require_GET
@render_to('core/show_academy.html')
def show_academy(request):
    """
    超级管理员 配置学院页面
    :param request:
    :return:
    """
    user = request.user
    if not user.is_superuser:
        raise Http404
    academy_all = Academy.objects.all()
    paginator = Paginator(academy_all, 10)
    page_num = request.GET.get('page')
    try:
        academy_all = paginator.page(page_num)
    except PageNotAnInteger:
        academy_all = paginator.page(1)
    except EmptyPage:
        academy_all = paginator.page(paginator.num_pages)
    system_info = "超级管理员"
    return {'academy_all': academy_all, 'system_info': system_info, 'user': user}


@require_GET
@render_to('core/show_group.html')
def show_group(request):
    """
    权限组
    :param request:
    :return:
    """
    user = request.user
    if not user.is_superuser:
        raise Http404
    group_all = Group.objects.all()
    system_info = "超级管理员"
    return {'group_all': group_all, 'system_info': system_info, 'user': user}


@require_GET
@render_to('core/show_instructor.html')
def show_instructor(request):
    """
    学院管理员 配置 老师
    :param request:
    :return:
    """
    user = request.user
    admin_match = get_user_admin(user)
    if not admin_match:
        raise Http404
    # TODO 需要判断哪个学院
    academy = admin_match.academy
    instructor_all = Instructor.objects.filter(academy=academy)
    speciality_all = Speciality.objects.filter(academy=academy)
    system_info = academy.name
    return {'instructor_all': instructor_all, 'speciality_all': speciality_all, 'system_info': system_info,
            'admin': admin_match}


@require_GET
@render_to('core/show_student.html')
def show_student(request):
    # TODO login_required 权限
    """
    学院管理员 配置 学生
    :param request:
    :return:
    """
    user = request.user
    admin_match = get_user_admin(user)
    if not admin_match:
        raise Http404
    academy = admin_match.academy
    student_all = Student.objects.filter(academy=academy)
    speciality_all = Speciality.objects.filter(academy=academy)
    system_info = academy.name
    return {'student_all': student_all, 'speciality_all': speciality_all, 'system_info': system_info,
            'admin': admin_match}


@require_GET
@render_to('core/show_thesis.html')
def show_thesis(request):
    """
    学院管理员 配置选题
    :param request:
    :return:
    """
    user = request.user
    admin_match = get_user_admin(user)
    if not admin_match:
        raise Http404
    academy = Admin.objects.get(user=user).academy
    thesis_all = Thesis.objects.filter(academy=academy)
    instructor_all = Instructor.objects.filter(academy=academy)
    system_info = academy.name
    status_all = Thesis.THESIS_STATUS
    for item in thesis_all:
        item.status = (item.status, item.get_status_display())
    return {'thesis_all': thesis_all, 'instructor_all': instructor_all, 'admin': admin_match,
            'status_all': status_all, 'system_info': system_info}


@require_GET
@login_required
@render_to('core/show_papersection.html')
def show_papersection(request):
    """
    学院管理员 查看选题结果
    :return:
    """
    user = request.user
    admin_match = get_user_admin(user)
    if not admin_match:
        raise Http404
    academy = Admin.objects.get(user=user).academy
    paper_all = PaperSection.objects.filter(thesis__academy=academy)
    for item in paper_all:
        item.thesis.status = (item.thesis.status, item.thesis.get_status_display())
    system_info = academy.name
    return {'paper_all': paper_all, 'admin': admin_match, 'system_info': system_info}


@require_GET
@render_to('core/show_thesis_self.html')
def show_thesis_self(request):
    """
    教师 配置选题
    :param request:
    :return:
    """
    # TODO 检查权限
    user = request.user
    instructor_match = get_user_instructor(user)
    if not instructor_match:
        raise Http404
    academy = instructor_match.academy
    thesis_all = Thesis.objects.filter(instructor=instructor_match)
    system_info = academy.name
    status_all = Thesis.THESIS_STATUS
    for item in thesis_all:
        item.status = (item.status, item.get_status_display())
    return {'thesis_all': thesis_all, 'system_info': system_info, 'instructor': instructor_match,
            'status_all': status_all}


@require_GET
@render_to('core/show_thesis_single.html')
def show_thesis_single(request):
    """
    学生 论文选题
    :param request:
    :return:
    """
    user = request.user
    student_match = get_user_student(user)
    if not student_match:
        raise Http404
    academy = student_match.academy
    thesis_all = Thesis.objects.filter(academy=academy)
    system_info = academy.name
    for item in thesis_all:
        item.status = (item.status, item.get_status_display())
    return {'thesis_all': thesis_all, 'system_info': system_info, 'student': student_match}


@require_GET
@login_required
@render_to('core/show_papersection_single.html')
def show_papersection_single(request):
    """
    学生 查看选课结果
    :param request:
    :return:
    """
    # TODO 检查权限
    user = request.user
    student_match = get_user_student(user)
    if not student_match:
        raise Http404
    academy = student_match.academy
    papersection = PaperSection.objects.get(student=student_match)
    papersection.thesis.status = (papersection.thesis.status, papersection.thesis.get_status_display())
    system_info = academy.name
    return {'paper': papersection, 'system_info': system_info, 'student': student_match}


@require_GET
@render_to('core/show_papersection_self.html')
def show_papersection_self(request):
    """
    教师 查看选课结果
    :param request:
    :return:
    """
    # TODO 检查权限
    user = request.user
    instructor_match = get_user_instructor(user)
    if not instructor_match:
        raise Http404
    academy = instructor_match.academy
    papersection_all = PaperSection.objects.filter(thesis__instructor=instructor_match,
                                                   thesis__status=Thesis.THESIS_STATUS[3][0])
    for item in papersection_all:
        item.thesis.status = (item.thesis.status, item.thesis.get_status_display())
    system_info = academy.name
    return {'paper_all': papersection_all, 'system_info': system_info, 'instructor': instructor_match}







