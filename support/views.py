import datetime

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render
from .models import *
from .forms import *
from .utils import *
import openpyxl


# Create your views here.
def home(request):
	return render(request, 'support/home.html')


def update_price_list(request, pl_id):
	if request.user.role.price_list_update_list_permission:
		if request.method == 'GET':
			return render(request, 'support/update_price_list.html', {
				'form': PriceListForm(),
				'pl': PriceList.objects.get(id=pl_id)
			})

		elif request.method == 'POST':

			pl = PriceList.objects.get(id=pl_id)

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

				Product.objects.filter(pricelist__id=pl_id).delete()
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
							pricelist=pl,
							serial=sn_,
							name=name_,
							count=ost_,
							price=prc_,
							manufacturer=mrk_,
						)

				Activity.objects.create(
					user=request.user,
					act='Обновление прайс-листа'
				)

				pl.last_update = datetime.datetime.now()
				pl.save()

				return HttpResponseRedirect(f'/pricelist/{pl_id}')


def pricelists(request):
	if request.user.role.price_list_view_list_permission:
		pls = PriceList.objects.all()

		return render(request, 'support/pricelists.html', {
			'pls': pls
		})


def pricelist(request,  pl_id):
	if request.user.role.price_list_view_list_permission:
		if request.method == 'GET':
			pl = PriceList.objects.get(id=pl_id)

			products = Product.objects.filter(pricelist=pl)
			update_date = pl.last_update

			return render(request, 'support/pricelist.html', {
				'products': products,
				'update_date': update_date,
				'pricelist': pl
			})

		elif request.method == 'POST':
			pl = PriceList.objects.get(id=pl_id)
			products = Product.objects.filter(pricelist=pl)

			if request.POST['search']:
				products = [
					x for x in products if
					request.POST['search'].lower() in str(x.serial).lower() or
					request.POST['search'].lower() in str(x.name).lower() or
					request.POST['search'].lower() in str(x.manufacturer).lower() or
					request.POST['search'].lower() in str(x.price).lower()
				]

			if request.POST['serial']:
				products = [x for x in products if request.POST['serial'].lower() in str(x.serial).lower()]
			if request.POST['name']:
				products = [x for x in products if request.POST['name'].lower() in str(x.name).lower()]
			if request.POST['manufacturer']:
				products = [x for x in products if request.POST['manufacturer'].lower() in str(x.manufacturer).lower()]
			if request.POST['price']:
				products = [x for x in products if request.POST['price'].lower() in str(x.price).lower()]

			return render(request, 'support/pricelist.html', {
				'products': products,
				'update_date': pl.last_update,
				'pricelist': pl
			})


def files(request):
	if request.user.role.file_sharing_download_file_permission:
		if request.method == 'GET':

			folders = Folder.objects.filter(parent_folder=None)
			docs = Document.objects.filter(folder=None)

			return render(request, 'support/files.html', {
				'folders': folders,
				'docs': docs
			})


def folder(request, folder_id):
	folder_ = Folder.objects.get(id=folder_id)
	docs = Document.objects.filter(folder=folder_)
	folders = Folder.objects.filter(parent_folder=folder_)

	class PathStep:
		def __init__(self, path, id_):
			self.path = path
			self.id_ = id_

	path = [PathStep(folder_.name, folder_.id)]
	f = folder_.parent_folder
	while f:
		path.append(PathStep(f.name, f.id))
		f = f.parent_folder

	return render(request, 'support/folder.html', {
		'path': path[::-1],
		'folders': folders,
		'docs': docs,
		'folder_id': folder_id
	})


def create_doc_without(request):
	if request.user.role.file_sharing_create_file_permission:
		if request.method == 'GET':
			return render(request, 'support/create_doc.html', {'form': CreateDocForm()})
		elif request.method == 'POST':
			form = CreateDocForm(request.POST, request.FILES)
			if form.is_valid():
				doc = form.save(commit=False)
				doc.creator = request.user

				types = {
					'pdf': 'pdf',
					'xlsx': 'excel',
					'xls': 'excel',
					'docx': 'docx',
					'doc': 'docx',
					'png': 'image',
					'jpg': 'image',
					'jpeg': 'image',
				}

				if doc.file.path.split('.')[-1] in types:
					doc.doctype = types[doc.file.path.split('.')[-1]]
				else:
					doc.doctype = 'uncknown'

				doc.save()

				Activity.objects.create(
					user=request.user,
					act=f'Создание файла "{doc.name}"'
				)

				return HttpResponseRedirect('/files')
			else:
				return render(request, 'support/create_doc.html', {'form': form})


def create_folder_without(request):
	if request.user.role.file_sharing_create_folder_permission:
		if request.method == 'GET':
			return render(request, 'support/create_folder.html')
		elif request.method == 'POST':
			name = request.POST['name']

			Folder.objects.create(
				name=name,
				creator=request.user,
				parent_folder=None
			)

			Activity.objects.create(
				user=request.user,
				act=f'Создание папки "{name}"'
			)

			return HttpResponseRedirect('/files')


def create_doc_on_folder(request, fid):
	if request.user.role.file_sharing_create_file_permission:
		if request.method == 'GET':
			return render(request, 'support/create_doc.html', {'form': CreateDocForm()})
		elif request.method == 'POST':
			form = CreateDocForm(request.POST, request.FILES)
			if form.is_valid():
				doc = form.save(commit=False)
				doc.creator = request.user
				doc.folder = Folder.objects.get(id=fid)

				types = {
					'pdf': 'pdf',
					'xlsx': 'excel',
					'xls': 'excel',
					'docx': 'docx',
					'doc': 'docx',
					'png': 'image',
					'jpg': 'image',
					'jpeg': 'image',
				}

				if doc.file.path.split('.')[-1] in types:
					doc.doctype = types[doc.file.path.split('.')[-1]]
				else:
					doc.doctype = 'uncknown'

				doc.save()

				Activity.objects.create(
					user=request.user,
					act=f'Создание документа "{doc.name}"'
				)

				return HttpResponseRedirect(f'/files/folder/{fid}')
			else:
				return render(request, 'support/create_doc.html', {'form': form})


def create_folder_on_folder(request, fid):
	if request.user.role.file_sharing_create_folder_permission:
		if request.method == 'GET':
			return render(request, 'support/create_folder.html')
		elif request.method == 'POST':
			name = request.POST['name']

			Folder.objects.create(
				name=name,
				creator=request.user,
				parent_folder=Folder.objects.get(id=fid)
			)

			Activity.objects.create(
				user=request.user,
				act=f'Создание папки "{name}"'
			)

			return HttpResponseRedirect(f'/files/folder/{fid}')


def create_pricelist(request):
	if request.user.role.price_list_create_list_permission:
		if request.method == 'GET':
			return render(request, 'support/create_pricelist.html')

		if request.method == 'POST':
			pl = PriceList.objects.create(
				name=request.POST['name'],
				last_update=datetime.datetime.now()
			)

			Activity.objects.create(
				user=request.user,
				act=f'Создание прайс-листа "{pl.name}"'
			)

			return HttpResponseRedirect(f'/pricelist/{pl.id}')


def delete_pricelist(request, pl_id):
	if request.user.role.price_list_delete_list_permission:

		pl = PriceList.objects.filter(id=pl_id)
		if len(pl):
			pl = pl[0]
			pl.delete()

			Activity.objects.create(
				user=request.user,
				act=f'Создание прайс-листа "{pl.name}"'
			)

		return HttpResponseRedirect('/pricelists')


def activitys(request):
	users = CustomUser.objects.filter(
		role__in=request.user.role.activity_view_permission.all()
	)
	roles = [
		x for x in request.user.role.activity_view_permission.all() if
		len([i for i in users if i.role == x])
	]

	if len(roles):
		return render(request, 'support/activitys.html', {
			'roles': roles,
			'users': users
		})


def user_activity(request, uid):
	user = CustomUser.objects.get(id=uid)

	if user.role in request.user.role.activity_view_permission.all():
		acts = Activity.objects.filter(user=user)
		return render(request, 'support/user_acts.html', {
			'user': user,
			'acts': acts[::-1]
		})


def download_user_activity(request, uid):
	user = CustomUser.objects.get(id=uid)

	if user.role in request.user.role.activity_view_permission.all():
		acts = Activity.objects.filter(user=user)[::-1]
		path = os.path.join(settings.BASE_DIR, f'media/tmp/users_acts/acts_{request.user.id}_{user.id}.xlsx')

		workbook = openpyxl.Workbook()
		worksheet = workbook.active

		worksheet.append(['Активности пользователя', f'{user.username} {user.email}'])

		for act in acts:
			worksheet.append([str(act.date), act.act])

		workbook.save(path)
		file = open(path, 'rb')
		return FileResponse(file)


def contacts(request):
	if request.user.role.contacts_view_permission:
		users = []

		for user in CustomUser.objects.all():
			if user.role in request.user.role.contacts_can_view_permission.all():
				users.append(user)

		return render(request, 'support/contacts.html', {
			'users': users,
			'roles': set([x.role for x in users])
		})


@csrf_exempt
def remove_document(request):
	if request.user.role.file_sharing_delete_document_permission:
		if request.method == 'POST':
			try:
				doc = Document.objects.get(id=int(request.POST['doc_id']))
				doc.delete()

				Activity.objects.create(
					user=request.user,
					act=f'Удаление документа "{doc.name}"'
				)

				return HttpResponse(status=200)
			except:
				return HttpResponse(status=400)


@csrf_exempt
def remove_folder(request):
	if request.user.role.file_sharing_delete_folder_permission:

		if request.method == 'POST':
			try:
				folder = Folder.objects.get(id=int(request.POST['folder_id']))
				folder.delete()

				Activity.objects.create(
					user=request.user,
					act=f'Удаление папки "{folder.name}"'
				)

				return HttpResponse(status=200)
			except:
				return HttpResponse(status=400)
