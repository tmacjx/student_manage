# coding=utf-8
from django.contrib.auth.models import User
from core.models import Student, Instructor, Admin


def get_user_student(user):
    try:
        student = Student.objects.get(user=user)
    # TODO 自定义异常类型
    except Exception, e:
        return None
    return student


def get_user_instructor(user):
    try:
        instructor = Instructor.objects.get(user=user)
    except Exception, e:
        return None
    return instructor


def get_user_admin(user):
    try:
        admin = Admin.objects.get(user=user)
    except Exception, e:
        return None
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
    if Student.objects.exists(user=user):
        return True
    else:
        return False


def is_admin(user):
    if Admin.objects.exists(user=user):
        return True
    else:
        return False


def is_instructor(user):
    if Instructor.objects.exists(user=user):
        return True
    else:
        return False


def is_super_admin(user):
    if user.is_superuser:
        return True
    else:
        return False
