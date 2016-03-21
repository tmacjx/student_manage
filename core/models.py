# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings


class Speciality(models.Model):
    SPECIALITY_TYPE = (
        (0, u'哲学'),
        (1, u'经济学'),
        (2, u'法学'),
        (3, u'教育学'),
        (4, u'文学'),
        (5, u'历史学'),
        (6, u'理学'),
        (7, u'工学'),
        (8, u'农学'),
        (9, u'医学'),
        (10, u'军事学'),
        (11, u'管理学'),
    )

    ID = models.IntegerField(unique=True, verbose_name=u'专业ID')
    name = models.CharField(max_length=100, unique=True, verbose_name=u'专业名称')
    short_name = models.CharField(max_length=20, verbose_name=u'专业简称')
    type = models.SmallIntegerField(choices=SPECIALITY_TYPE, verbose_name=u'专业分类')


class Department(models.Model):
    ID = models.IntegerField(verbose_name=u'系ID')
    name = models.CharField(max_length=100, verbose_name=u'系名称')
    speciality = models.ForeignKey(Speciality, unique=True, verbose_name=u'专业')


class Academy(models.Model):
    ID = models.IntegerField(verbose_name=u'学院ID')
    name = models.CharField(max_length=100, verbose_name=u'学院名称')
    department = models.ForeignKey(Department, unique=True, verbose_name=u'系')


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    ID = models.IntegerField(unique=True, verbose_name=u'学生ID')
    name = models.CharField(max_length=100, verbose_name=u'学生名')
    image = models.ImageField(verbose_name=u'头像', upload_to='/avatar', blank=True, default='/avatar/default.jpg')
    academy = models.ForeignKey(Academy, verbose_name=u'所在学院')
    department = models.ForeignKey(Department, verbose_name=u'所在系')
    Speciality = models.ForeignKey(Speciality, verbose_name=u'专业')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号')

    class Meta:
        permissions = (
            ('view_student',   'Can see available student'),
            ('change_student', 'Can change available student'),
            ('delete_student', 'Can delete available student')
        )


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    ID = models.IntegerField(unique=True, verbose_name=u'教师ID')
    name = models.CharField(max_length=10, verbose_name=u'教师名')
    image = models.ImageField(verbose_name=u'头像', upload_to='/avatar', blank=True, default='/avatar/default.jpg')
    academy = models.ForeignKey(Academy, verbose_name=u'所在学院')
    department = models.ForeignKey(Department, verbose_name=u'所在系')
    Speciality = models.ForeignKey(Speciality, verbose_name=u'专业')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号')

    class Meta:
        permissions = (
            ('view_instructor',   'Can see available instructor'),
            ('change_instructor', 'Can see available instructor'),
            ('delete_instructor', 'Can delete available instructor'),
        )


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    ID = models.IntegerField(unique=True, verbose_name=u'管理员ID')
    name = models.CharField(max_length=10, verbose_name=u'管理员名称')
    image = models.ImageField(verbose_name=u'头像', upload_to='/avatar', blank=True, default='/avatar/default.jpg')
    academy = models.ForeignKey(Academy, verbose_name=u'所在学院')
    department = models.ForeignKey(Department, verbose_name=u'所在系')
    cellphone = models.CharField(max_length=15, verbose_name=u'手机号')

    class Meta:
        permissions = (
            ('view_admin',   'Can see admin'),
            ('change_admin', 'Can change admin'),
            ('delete_admin', 'Can delete admin'),
        )


class Thesis(models.Model):
    THESIS_STATUS = (
        (0, '未发布'),
        (1, '已发布'),
        (2, '未选中'),
        (3, '已选中'),
    )
    ID = models.IntegerField(unique=True, verbose_name=u'论文ID')
    title = models.CharField(max_length=200, verbose_name=u'论文题目')
    content = models.TextField(verbose_name=u'论文要求')
    instructor = models.ForeignKey(Instructor, verbose_name=u'辅导老师')
    academy = models.ForeignKey(Academy, verbose_name=u'所属学院')
    status = models.SmallIntegerField(choices=THESIS_STATUS, default=0, verbose_name=u'论文状态')
    start_time = models.DateField(verbose_name=u'选题开始时间')
    end_time = models.DateField(verbose_name=u'选题结束时间')
    create_time = models.DateField(verbose_name=u'创建时间', auto_now_add=True)
    modify_time = models.DateField(verbose_name=u'修改时间', auto_now=True)

    class Meta:
        permissions = (
            ('view_thesis',   'Can see available thesis'),
            ('change_thesis', 'Can change available thesis'),
            ('delete thesis', 'Can delete available thesis')
        )


class PaperSection(models.Model):
    thesis = models.ForeignKey(Thesis, unique=True, verbose_name=u'论文选题')
    student = models.ForeignKey(Student, unique=True, verbose_name=u'学生')
    create_time = models.DateField(verbose_name=u'选中时间', auto_now_add=True)
    modify_time = models.DateField(verbose_name=u'改动时间', auto_now=True)
    # file = models.FileField(verbose_name=u'论文文档', blank=True)


class PaperDocuments(models.Model):
    DOCUMENT_TYPE = (
        (0, '开题报告'),
        (1, '外文翻译'),
        (2, '论文正稿'),
    )
    DOCUMENT_STATUS = (
        (0, '未上交'),
        (1, '已上交'),
    )
    # paper_section = models.ForeignKey(PaperSection, verbose_name=u'论文题目')
    thesis = models.ForeignKey(Thesis, verbose_name=u'论文选题')
    student = models.ForeignKey(Student, verbose_name=u'学生')
    type = models.SmallIntegerField(choices=DOCUMENT_TYPE, verbose_name=u'文档类型')
    status = models.SmallIntegerField(DOCUMENT_STATUS, verbose_name=u'文档状态')
    file = models.FileField(upload_to='/paper', verbose_name=u'文档')
    upload_time = models.DateTimeField(verbose_name=u'上交时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=u'修改时间', auto_now=True)

    class Meta:
        unique_together = ('thesis', 'student', 'type')




