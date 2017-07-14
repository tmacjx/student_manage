# coding=utf-8
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from util.functions import json_response, send_mail
from core.functions import check_user, is_super_admin, is_admin, is_instructor, is_student, get_user_by_email
from core.models import VerityCodeType, VerityCode, SuperAdmin, Admin, Student, Instructor, Academy,\
                                                                               Speciality, Thesis
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.db import transaction
from core.forms import SuperAdminForm, AdminForm, StudentForm, InstructorForm, SpecialityForm, \
    AcademyForm, EmailUserForm, ThesisForm, PaperSectionForm, GroupForm, CellPhoneForm, ForgetPwdForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseRedirect


@require_POST
def create_group(request):
    """
    新建权限组
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = GroupForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'新建成功'
    return json_response(result)


@require_POST
def delete_group(request):
    """
    删除权限组
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        with transaction.atomic():
            group_id = request.POST.get('group', '')
            group = Group.objects.get(id=group_id)
            group.delete()
    except Exception as e:
        result['msg'] = u'操作失败'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
def edit_group(request):
    """
    修改权限组
    :param request:
    :return:
    """
    pass


@require_POST
def create_academy(request):
    """
    新增学院
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = AcademyForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写错误'
        return json_response
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
def delete_academy(request):
    """
    删除学院
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        with transaction.atomic():
            academy_id = request.POST.get('academy', '')
            academy = Academy.objects.get(id=academy_id)
            academy.delete()
    except Exception as e:
        result['msg'] = u'表单错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
def create_speciality(request):
    """
    新建专业
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = SpecialityForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = '表单填写错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
def delete_speciality(request):
    """
    删除专业
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        with transaction.atomic():
            speciality_id = request.POST.get('speciality', '')
            speciality = Speciality.objects.get(id=speciality_id)
            speciality.delete()
    except Exception as e:
        result['msg'] = u'操作失败'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
def create_user(request):
    """
    新建用户,先建立user表,
    当用户激活邮箱后,再将user表关联到SuperAdmin Admin Instructor Student表
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form_email = EmailUserForm(request.POST)
    # 当邮箱已经存在 或者格式不正确时 is_valid() == False
    if form_email.is_valid():
        email = form_email.cleaned_data['email']
    else:
        result['msg'] = u'该邮箱已存在'
        return json_response(result)
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        result['msg'] = u'该用户已经存在'
        return json_response(result)
    else:
        try:
            with transaction.atomic():
                user = form.save(commit=False)
                # TODO 邮箱成功后, 才执行 user.save() 否则撤回?
                # user.email = email
                user.is_active = False
                # user.email = email
                user.save()
                vcode = VerityCode.objects.create(user=user, email=email
                                                  , code_type=VerityCodeType.ACTIVE_ACCOUNT)
                code = vcode.code
                send_mail(request, user, VerityCodeType.ACTIVE_ACCOUNT, code=code, to=email)
        except Exception as e:
            result['msg'] = u'激活邮件发送失败'
            return json_response(result)
    result['status'] = 1
    result['data']['user'] = user.id
    result['msg'] = u'注册成功, 请查收邮件'
    return json_response(result)


@require_POST
def create_superadmin(request):
    """
    新建超级管理员
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    # user = request.user
    form = SuperAdminForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写有误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'成功'
    return json_response(result)


@require_POST
def create_admin(request):
    """
    新建管理员
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    # user = request.user
    form = AdminForm(request.POST, request.FILES)
    # TODO 把user 添加到admin 权限组中
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写有误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'成功'
    return json_response(result)


@require_POST
def delete_admin(request):
    """
    删除管理员
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        with transaction.atomic():
            admin_id = request.POST.get('admin', '')
            admin = Admin.objects.get(id=admin_id)
            user = admin.user
            vcode = VerityCode.objects.filter(user=user)
            # 删除user关联的VerityCode
            vcode.delete()
            admin.delete()
            user.delete()
    except Exception as e:
        result['msg'] = u'操作失败'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
def create_instructor(request):
    """
    新建教师
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    # user = request.user
    form = InstructorForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写有误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'成功'
    return json_response(result)


@require_POST
def create_student(request):
    """
    新建学生
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = StudentForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写有误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'成功'
    return json_response(result)


@require_POST
def login(request):
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = AuthenticationForm(request, request.POST)
    if not form.is_valid():
        result['msg'] = u'用户名或者密码错误'
        return json_response(result)
    user = form.get_user()
    if not user.is_active:
        result['msg'] = u'该账户未激活,请先使用邮箱链接进行激活'
        return json_response(result)
    # if not check_user(user):
    #     result['msg'] = u'该用户不存在'
    #     return json_response(result)
    if is_super_admin(user):
        result['data']['next'] = '/superadmin/'
    elif is_admin(user):
        result['data']['next'] = '/secretary/'
    elif is_instructor(user):
        result['data']['next'] = '/instructor/'
        # return HttpResponseRedirect(reverse('instructor'))
    elif is_student(user):
        result['data']['next'] = '/student/'
    else:
        result['msg'] = '该用户不存在'
        return json_response(result)
    auth_login(request, user)
    result['status'] = 1
    result['msg'] = u'登录成功'
    return json_response(result)


@require_POST
@login_required
def logout(request):
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        auth_logout(request)
    except Exception as e:
        result['msg'] = u'登出失败'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'登出成功'
    return json_response(result)


@require_POST
def forget_pwd(request):
    """
    忘记密码, 发送重置链接到邮箱
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = ForgetPwdForm(request.POST)
    if not form.is_valid():
        result['msg'] = u'邮箱格式不正确'
        return json_response(result)
    email = form.cleaned_data['email']
    user = get_user_by_email(email)
    if not user:
        result['msg'] = u'不存在该邮箱的用户'
        return json_response(result)
    vcode = VerityCode.objects.create(user=user, code_type=VerityCodeType.FORGET_PWD, email=user.email)
    code = vcode.code
    try:
        send_mail(request, user, VerityCodeType.FORGET_PWD, code=code, to=email)
    except Exception as e:
        result['msg'] = u'发送邮件失败'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'邮件发送成功, 请注意查收'
    return json_response(result)


@require_POST
def reset_pwd(request):
    """
    重置密码
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    user = request.user
    form = SetPasswordForm(user, request.POST)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'重置密码成功'
    return json_response(result)


@require_POST
@login_required
def change_pwd(request):
    """
    修改密码
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    user = request.user
    form = PasswordChangeForm(user, request.POST)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'密码修改成功'
    return json_response(result)


@require_POST
@login_required
def perfect_admin(request):
    """
    修改admin资料
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    user = request.user
    try:
        admin = Admin.objects.get(user=user)
        form = AdminForm(request.POST, request.FILES, instance=admin)
    # TODO AdminDoesNotExist 如何细化异常类型
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
@login_required
def perfect_instructor(request):
    """
    修改Instructor资料
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    user = request.user
    try:
        instructor = Instructor.objects.get(user=user)
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    if form.is_valid():
        form.save()
    else:
        result['msg'] = u'表单填写错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
@login_required
def perfect_student(request):
    """
    修改Student资料
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    user = request.user
    try:
        student = Student.objects.get(user=user)
        form = StudentForm(request.POST, request.FILES, instance=student)
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    if form.is_valid():
        form.save()
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


# TODO 权限判断
# TODO 只有超级管理员 有权限
@require_POST
def delete_admin(request):
    """
    删除admin用户
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        admin_id = request.POST.get('admin', '')
        admin = Admin.objects.get(id=admin_id)
        admin.delete()
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'删除成功'
    return json_response(result)


# TODO 权限判断
# TODO 只有管理员 有权限
@require_POST
def delete_instructor(request):
    """
    删除Instructor用户
    :param request:
    :return:
    """
    # TODO 检查权限??  只能删除本学院的老师
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        with transaction.atomic():
            instructor_id = request.POST.get('instructor', '')
            instructor = Instructor.objects.get(id=instructor_id)
            user = instructor.user
            vcode = VerityCode.objects.filter(user=user)
            vcode.delete()
            instructor.delete()
            user.delete()
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'删除成功'
    return json_response(result)


# TODO 权限判断
# TODO 只有管理员 有权限
@require_POST
def delete_student(request):
    """
    删除Student用户
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        student_id = request.POST.get('student', '')
        student = Student.objects.get(id=student_id)
        user = student.user
        vcode = VerityCode.objects.filter(user=user)
        vcode.delete()
        student.delete()
        user.delete()
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'删除成功'
    return json_response(result)


@require_POST
def get_speciality(request):
    """
    根据学院, 查询专业
    :param request:
    :return:
    """
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        academy_id = request.POST.get('academy', '')
        academy = Academy.objects.get(id=academy_id)
        speciality_list = Speciality.objects.filter(academy=academy)
    except Exception as e:
        result['msg'] = u'Inner Error'
        return json_response(result)
    # TODO 是否有更好的方案 {'id': name, }
    tmp_dict = {}
    for speciality in speciality_list:
        tmp_dict[str(speciality.id)] = speciality.name
    result['data'] = tmp_dict
    result['status'] = 1
    result['msg'] = u'成功'
    return json_response(result)


# TODO 权限判断
# TODO 只有本学院的老师才可以新建论文题目, 并且instructor academy 前端为disable的,
# TODO 默认新增的论文状态都为未选中
@require_POST
def create_thesis(request):
    """
    学院管理员 新增选题
    :param request:
    :return:
    """
    # TODO 判断权限 只能学院管理员 新建选题
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = ThesisForm(request.POST)
    if form.is_valid():
        # TODO 表单错误常见类型 论文已存在, 论文题目重复, 有的选项没有填写
        form.save()
    else:
        result['msg'] = u'表单错误'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'新增成功'
    return json_response(result)


@require_POST
def delete_thesis(request):
    """
    学院管理员 删除选题
    :param request:
    :return:
    """
    # TODO 只能删除本学院的选题
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    try:
        with transaction.atomic():
            thesis_id = request.POST.get('thesis', '')
            thesis = Thesis.objects.get(id=thesis_id)
            thesis.delete()
    except Exception as e:
        result['msg'] = u'Innor Error'
        return json_response(result)
    result['status'] = 1
    result['msg'] = u'操作成功'
    return json_response(result)


@require_POST
@login_required
def choice_thesis(request):
    """
    学生 论文选题
    :param request:
    :return:
    """
    # TODO 检查权限 只有学生可以选题, 只可以选择本学院的题目
    result = {"status": 0, "apiVersion": "1.0", "msg": "", "data": {}}
    form = PaperSectionForm(request.POST)
    if form.is_valid():
        paper = form.save(commit=False)
    else:
        result['msg'] = u'选题失败'
        return json_response(result)
    try:
        with transaction.atomic():
            thesis = paper.thesis
            thesis.status = Thesis.THESIS_STATUS[3][0]
            thesis.save()
            paper.save()
    except Exception as e:
        result['msg'] = u"Inner Error"
        return json_response(result)
    result['status'] = 1
    result['msg'] = u"选题成功"
    return json_response(result)









