# coding=utf-8
from django.contrib.auth.models import User
from core.models import Student, Instructor, Admin, SuperAdmin


def get_user_student(user):
    try:
        student = Student.objects.get(user=user)
    # TODO 自定义异常类型
    except Exception, e:
        return None
    else:
        return student


def get_user_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)
    except Exception, e:
        return None
    else:
        return instructor


def get_user_admin(user):
    try:
        admin = Admin.objects.get(user=user)
    except Exception, e:
        return None
    else:
        return admin


def check_user(user):
    if get_user_admin(user):
        return True
    if get_user_instructor(user):
        return True
    if get_user_student(user):
        return True
    return False


def is_student(user):
    if Student.objects.filter(user=user).exists():
        return True
    else:
        return False


def is_admin(user):
    if Admin.objects.filter(user=user).exists():
        return True
    else:
        return False


def is_instructor(user):
    if Instructor.objects.filter(user=user).exists():
        return True
    else:
        return False


def is_super_admin(user):
    if SuperAdmin.objects.filter(user=user).exists():
        return True
    else:
        return False


def get_user_by_email(email):
    # if User.objects.filter(email=email).exists():
    #     return True
    # else:
    #     return False
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        return None
    else:
        return user

