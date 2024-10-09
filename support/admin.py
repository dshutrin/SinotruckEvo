from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'name', 'surname', 'role')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_display = ('name', )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
	list_display = ('date', 'user', 'act')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
	list_display = ('name', )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ('name', )

