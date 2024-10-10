from django.forms import *
from django.core.validators import FileExtensionValidator
from .models import *


class PriceListForm(Form):
	file = FileField(label='xlsx файл', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])


class CreateDocForm(ModelForm):
	class Meta:
		model = Document
		exclude = ['creator', 'doctype', 'folder']
