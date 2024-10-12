from django.forms import *
from django import forms
from django.core.validators import FileExtensionValidator
from .models import *


class PriceListForm(Form):
	file = FileField(label='xlsx файл', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])


class CreateDocForm(ModelForm):
	class Meta:
		model = Document
		exclude = ['creator', 'doctype', 'folder']


class EditUserForm(Form):

	username = CharField(max_length=255, label='Имя пользователя')
	clear_password = CharField(max_length=255, label='Пароль')
	name = CharField(max_length=255, label='ФИО/Название организации')
	phone = CharField(max_length=12, label='Номер телефона')
	manager_task = CharField(max_length=255, label='Задача менеджера')
	role = forms.ChoiceField(choices=(
		(x.id, x.name) for x in Role.objects.all()
	))


class UserCreationForm(ModelForm):
	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'clear_password', 'name', 'phone', 'manager_task', 'role']
