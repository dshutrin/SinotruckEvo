from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *
from .utils import *
import openpyxl


# Create your views here.
def home(request):
	return render(request, 'support/home.html')


def update_price_list(request):
	if request.user.role.price_list_update_list_permission:
		if request.method == 'GET':
			return render(request, 'support/update_price_list.html', {
				'form': PriceListForm()
			})

		elif request.method == 'POST':
			f = request.FILES["excel_file"]
			end = request.FILES["excel_file"].name.split(".")[-1]

			if end in ['xlsx', 'xls']:
				path = os.path.join(settings.BASE_DIR, f'media/pricelist/file.{end}')
				with open(path, 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)

				fix_excel(path)

				excel = openpyxl.load_workbook(path)
				sheet = excel.active

				rows = []
				for r in sheet.rows:
					rows.append([])
					for cell in r:
						rows[-1].append(cell.value)

				start_index = 0
				for i in range(len(rows)):
					if 'Номенклатура.Артикул' in [str(x).strip() for x in rows[i] if x]:
						start_index = i
						break

				dt = [str(x).strip() for x in rows[start_index]]
				sn = dt.index('Номенклатура.Артикул')
				name = dt.index('Ценовая группа/ Номенклатура')
				ost = dt.index('Остаток')
				mrk = dt.index('Марки')
				prc = dt.index('Дилер')

				Product.objects.all().delete()
				for row in rows[start_index + 1:]:
					sn_ = row[sn]
					if sn_:
						name_ = row[name]
						ost_ = str(row[ost])
						if ost_.isdigit():
							ost_ = int(ost_)

						mrk_ = row[mrk]
						prc_ = str(row[prc]).replace('руб.', '').strip()
						if prc_.replace('.', '').isdigit():
							prc_ = float(prc_)

						Product.objects.create(
							serial=sn_,
							name=name_,
							count=ost_,
							price=prc_,
							manufacturer=mrk_
						)

				Activity.objects.create(
					user=request.user,
					act='Обновление прайс-листа'
				)

				return HttpResponseRedirect('/pricelist')


def pricelist(request):
	if request.method == 'GET':

		if request.user.role.price_list_view_list_permission:
			products = Product.objects.all()
			update_date = Activity.objects.filter(act='Обновление прайс-листа').order_by('-date').first().date

			return render(request, 'support/pricelist.html', {
				'products': products,
				'update_date': update_date
			})
