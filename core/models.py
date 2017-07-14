# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone
import hashlib
import random
import datetime


class VerityCodeType(object):
    """
    邮箱验证码类型
    ACTIVE_ACCOUNT 激活账户
    FORGET_PWD     忘记密码
    """
    ACTIVE_ACCOUNT, FORGET_PWD, RESET_PWD = xrange(1, 4)


class VerityCode(models.Model):
    """邮箱验证码"""

    CODE_TYPE_CHOICES = (
        (VerityCodeType.ACTIVE_ACCOUNT, u'激活账户'),
        (VerityCodeType.FORGET_PWD, u'忘记密码'),
        (VerityCodeType.RESET_PWD, u'重置密码'),
    )

    # 验证码过期时间
    _CODE_EXPIRE_DAYS = 1

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    email = models.EmailField(verbose_name=u'邮箱')
    code = models.CharField(null=True, max_length=32, verbose_name=u'验证码')
    code_type = models.SmallIntegerField(choices=CODE_TYPE_CHOICES, verbose_name=u'验证码类型')
    is_used = models.BooleanField(verbose_name=u'是否已经使用', default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(verbose_name=u'过期时间')

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        if not self.expire_time:
            self.expire_time = timezone.now() + datetime.timedelta(days=self._CODE_EXPIRE_DAYS)
        return super(VerityCode, self).save(*args, **kwargs)

    def generate_code(self):
        m = hashlib.md5()
        m.update(self.email)
        m.update(str(timezone.now()))
        m.update(str(random.random()))
        return m.hexdigest()


class Academy(models.Model):
    """
    院系
    """
    index = models.IntegerField(unique=True, verbose_name=u'学院ID')
    name = models.CharField(max_length=100, verbose_name=u'学院名称')
    short_name = models.CharField(unique=True, max_length=20, verbose_name=u'学院简称')


class Speciality(models.Model):
    """
    专业
    """
    index = models.IntegerField(unique=True, verbose_name=u'专业ID')
    name = models.CharField(max_length=100, unique=True, verbose_name=u'专业名称')
    short_name = models.CharField(max_length=20, verbose_name=u'专业简称')
    academy = models.ForeignKey(Academy, verbose_name=u'所属学院')


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    index = models.IntegerField(unique=True, verbose_name=u'学生ID')
    name = models.CharField(max_length=100, verbose_name=u'学生名')
    image = models.ImageField(verbose_name=u'头像', upload_to='/avatar', blank=True, default='/avatar/default.jpg')
    academy = models.ForeignKey(Academy, verbose_name=u'所在学院')
    speciality = models.ForeignKey(Speciality, verbose_name=u'专业')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号', default='')

    @property
    def image_url(self):
        try:
            img = open(self.image.path, "rb")
            data = img.read()
            return "data:image/jpg;base64,%s" % data.encode('base64')
        except IOError:
            return self.image.url


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    index = models.IntegerField(unique=True, verbose_name=u'教师ID')
    name = models.CharField(max_length=10, verbose_name=u'教师名')
    image = models.ImageField(verbose_name=u'头像', upload_to='/avatar', blank=True, default='/avatar/default.jpg')
    academy = models.ForeignKey(Academy, verbose_name=u'所在学院')
    speciality = models.ForeignKey(Speciality, verbose_name=u'专业')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号', default='')

    @property
    def image_url(self):
        try:
            img = open(self.image.path, "rb")
            data = img.read()
            return "data:image/jpg;base64,%s" % data.encode('base64')
        except IOError:
            return self.image.url


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    index = models.IntegerField(unique=True, verbose_name=u'管理员ID')
    name = models.CharField(max_length=10, verbose_name=u'管理员名称')
    image = models.ImageField(verbose_name=u'头像', upload_to='/avatar', blank=True, default='/avatar/default.jpg')
    academy = models.ForeignKey(Academy, verbose_name=u'所在学院')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号', default='')

    # TODO 需要测试下 {{ item.image_url }}    {{ item.image.url }}
    @property
    def image_url(self):
        try:
            img = open(self.image.path, "rb")
            data = img.read()
            return "data:image/jpg;base64,%s" % data.encode('base64')
        except IOError:
            return self.image.url


class SuperAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=10, verbose_name='超级管理员名称')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号', default='')


class Thesis(models.Model):
    THESIS_STATUS = (
        (0, '未发布'),
        (1, '已发布'),
        (2, '未选中'),
        (3, '已选中'),
    )
    # index = models.IntegerField(unique=True, verbose_name=u'论文ID')
    title = models.CharField(max_length=200, unique=True, verbose_name=u'论文题目')
    content = models.TextField(verbose_name=u'论文要求')
    instructor = models.ForeignKey(Instructor, verbose_name=u'辅导老师')
    academy = models.ForeignKey(Academy, verbose_name=u'所属学院')
    status = models.SmallIntegerField(choices=THESIS_STATUS, default=0, verbose_name=u'论文状态')
    start_time = models.DateTimeField(verbose_name=u'选题开始时间')
    end_time = models.DateTimeField(verbose_name=u'选题结束时间')
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)


class PaperSection(models.Model):
    # thesis = models.ForeignKey(Thesis, unique=True, verbose_name=u'论文选题')
    thesis = models.OneToOneField(Thesis, verbose_name=u'论文选题')
    student = models.OneToOneField(Student, verbose_name=u'学生')
    create_time = models.DateTimeField(verbose_name=u'选中时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=u'改动时间', auto_now=True)
    # file = models.FileField(verbose_name=u'论文文档', blank=True)


class PaperDocuments(models.Model):
    DOCUMENT_TYPE = (
        (0, '开题报告'),
        (1, '外文翻译'),
        (2, '论文正稿'),
    )
    DOCUMENT_STATUS = (
        (0, '未上传'),
        (1, '已上传'),
    )
    # paper_section = models.ForeignKey(PaperSection, verbose_name=u'论文题目')
    thesis = models.ForeignKey(Thesis, verbose_name=u'论文选题')
    student = models.ForeignKey(Student, verbose_name=u'学生')
    type = models.SmallIntegerField(choices=DOCUMENT_TYPE, verbose_name=u'文档类型')
    status = models.SmallIntegerField(choices=DOCUMENT_STATUS, verbose_name=u'文档状态')
    file = models.FileField(upload_to='/paper', verbose_name=u'文档')
    upload_time = models.DateTimeField(verbose_name=u'上交时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)

    class Meta:
        unique_together = ('thesis', 'student', 'type')


class PaperDemo(models.Model):
    DOCUMENT_TYPE = (
        (0, '开题报告'),
        (1, '外文翻译'),
        (2, '论文正稿'),
    )
    DOCUMENT_STATUS = (
        (0, '未上传'),
        (1, '已上传'),
    )
    thesis = models.ForeignKey(Thesis, verbose_name=u'论文选题')
    type = models.SmallIntegerField(choices=DOCUMENT_TYPE, verbose_name=u'文档范例类型')
    status = models.SmallIntegerField(choices=DOCUMENT_STATUS, verbose_name=u'文档范例状态')
    title = models.CharField(max_length=100, verbose_name=u'文档范例标题')
    file = models.FileField(blank=True, upload_to='/paper_demo', verbose_name=u'文档范例链接')
    upload_time = models.DateTimeField(verbose_name=u'上传时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)

    class Meta:
        unique_together = ('thesis', 'type')




