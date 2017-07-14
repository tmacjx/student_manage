# coding=utf-8
from core.models import SuperAdmin, Admin, Student, Instructor, Speciality, Academy, Thesis, PaperSection
from django import forms
from localflavor.cn.forms import CNCellNumberField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


class EmailUserForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            msg = u"该邮箱已存在"
            self.add_error('email', msg)
        else:
            return self.cleaned_data['email']


class ForgetPwdForm(forms.Form):
    email = forms.EmailField()


class CellPhoneForm(forms.Form):
    """中国区手机号码"""
    cellphone = CNCellNumberField(required=False)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = '__all__'


class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['image', 'cellphone']


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        exclude = ['image', 'cellphone']


class AdminForm(forms.ModelForm):

    # def clean_cellphone(self):
    #     cellphone = self.cleaned_data['cellphone']
    #
    class Meta:
        model = Admin
        # fields = '__all__'
        exclude = ['image', 'cellphone']


class SuperAdminForm(forms.ModelForm):
    class Meta:
        model = SuperAdmin
        fields = '__all__'


class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = '__all__'


class PaperSectionForm(forms.ModelForm):
    class Meta:
        model = PaperSection
        fields = '__all__'
