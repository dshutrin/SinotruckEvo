from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import *


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

	# Прайс-лист
	price_list_update_list_permission = models.BooleanField(
		default=False, verbose_name="Возможность обновлять прайс-лист")
	price_list_download_list_permission = models.BooleanField(
		default=False, verbose_name="Возможность скачивать прайс-лист")
	price_list_view_list_permission = models.BooleanField(
		default=False, verbose_name="Возможность просматривать прайс-лист (Влияет на доступ к меню)")

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


class CustomUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(verbose_name='Имя пользователя', max_length=150, null=False, default=None, unique=True)
	email = models.EmailField(unique=True, null=True, default=None, blank=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	name = models.CharField(verbose_name='Имя', max_length=150, null=True, default=None)
	surname = models.CharField(verbose_name='Фамилия', max_length=150, null=True, default=None, blank=True)
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
		return f'{self.name} {self.surname}'

	class Meta:
		db_table = 'auth_user'
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return f'{self.name} {self.surname}'



