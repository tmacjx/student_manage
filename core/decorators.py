from core.functions import is_admin, is_instructor, is_student, is_super_admin
from django.contrib.auth import REDIRECT_FIELD_NAME


def auth_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    pass
