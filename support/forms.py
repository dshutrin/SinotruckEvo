from django.forms import *
from django.core.validators import FileExtensionValidator


class PriceListForm(Form):
	file = FileField(label='xlsx файл', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])
