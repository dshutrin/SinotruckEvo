from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .managers import *
import os


class Role(models.Model):
	name = models.CharField(max_length=50, unique=True, verbose_name="Роль")

	# Файлообменник
	file_sharing_create_file_permission = models.BooleanField(
		default=False, verbose_name="Возможность создавать файлы в файлообменнике")
	file_sharing_download_file_permission = models.BooleanField(
		default=False, verbose_name="Возможность скачивать файлы в файлообменнике (Влияет на доступ к меню)")
	file_sharing_create_folder_permission = models.BooleanField(
		default=False, verbose_name="Возможность создавать папки в файлообменнике")
	file_sharing_delete_folder_permission = models.BooleanField(
		default=False, verbose_name="Возможность удалять папки в файлообменнике")
	file_sharing_delete_document_permission = models.BooleanField(
		default=False, verbose_name="Возможность удалять файлы в файлообменнике")

	# Прайс-лист
	price_list_update_list_permission = models.BooleanField(
		default=False, verbose_name="Возможность обновлять прайс-лист")
	price_list_download_list_permission = models.BooleanField(
		default=False, verbose_name="Возможность скачивать прайс-лист")
	price_list_view_list_permission = models.BooleanField(
		default=False, verbose_name="Возможность просматривать прайс-лист (Влияет на доступ к меню)")
	price_list_create_list_permission = models.BooleanField(
		default=False, verbose_name='Возможность создавать прайс-листы')
	price_list_delete_list_permission = models.BooleanField(
		default=False, verbose_name='Возможность удалять прайс-листы')

	# История действий
	activity_view_permission = models.ManyToManyField(
		'Role', verbose_name="Чью активность разрешено просматривать (Влияет на доступ к меню)", blank=True)

	# Корзина
	trash_permission = models.BooleanField(
		default=False,
		verbose_name='Возможность добавлять товары в корзину и оставлять заявку заказов (Влияет на доступ к меню)')

	# Заказы
	order_view_permission = models.BooleanField(
		default=False, verbose_name="Возможность просматривать заявки заказов (Влияет на доступ к меню)")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Роль'
		verbose_name_plural = 'Роли'


class CustomUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(verbose_name='Имя пользователя', max_length=150, null=False, default=None, unique=True)
	email = models.EmailField(unique=True, null=True, default=None, blank=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	name = models.CharField(verbose_name='ФИО/Название организации', max_length=150, null=True, default=None)
	phone = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True, null=True, default=None, blank=True)
	manager_task = models.CharField(verbose_name='Задача менеджера', max_length=150, null=True, default=None, blank=True)
	role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, default=None, blank=True, verbose_name='Роль')

	objects = CustomUserManager()
	USERNAME_FIELD = 'username'

	def has_perm(self, perm, obj=None):
		return self.is_superuser

	def has_module_perms(self, app_label):
		return self.is_superuser

	def get_privs(self):
		return []

	def get_name(self):
		return f'{self.name}'

	class Meta:
		db_table = 'auth_user'
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return f'{self.name}'


class PriceList(models.Model):
	name = models.CharField(verbose_name='Наименование', max_length=255)
	creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
	last_update = models.DateTimeField(verbose_name='Последнее обновление')

	def __str__(self):
		return f'<{self.id}> "{self.name}"'

	class Meta:
		verbose_name = 'Прайс-лист'
		verbose_name_plural = 'Прайс-листы'


class Product(models.Model):
	pricelist = models.ForeignKey(PriceList, on_delete=models.CASCADE, null=False, default=None, blank=True)
	serial = models.CharField(max_length=100, verbose_name='Номенклатура.Артикул')
	count = models.PositiveIntegerField(verbose_name='Остаток', null=True)
	name = models.CharField(max_length=250, verbose_name='Ценовая группа/ Номенклатура', null=True)
	manufacturer = models.CharField(max_length=250, verbose_name='Марки', null=True)
	price = models.FloatField(verbose_name='Стоимость', null=True, default=None)

	def __str__(self):
		return f'{self.serial} {self.name}'

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'


class Activity(models.Model):
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата, время')
	user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
	act = models.CharField(max_length=255, verbose_name='Действие')

	class Meta:
		verbose_name = 'Активность'
		verbose_name_plural = 'Активности'


class Folder(models.Model):
	name = models.CharField(verbose_name='Название папки', max_length=150, unique=True)
	parent_folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)
	creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Папка'
		verbose_name_plural = 'Папки'


class Document(models.Model):
	name = models.CharField(verbose_name='Название документа', max_length=150, unique=True)
	folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
	file = models.FileField(upload_to='documents', verbose_name='Файл')
	creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
	doctype = models.CharField(verbose_name='Тип файла', max_length=10, default=None, null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Документ'
		verbose_name_plural = 'Документы'


@receiver(post_delete, sender=Document)
def delete_document(sender, instance, **kwargs):
	if os.path.exists(instance.file.path):
		os.remove(instance.file.path)
