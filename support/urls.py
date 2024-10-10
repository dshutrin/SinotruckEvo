from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('update_price_list/<int:pl_id>', update_price_list),
    path('pricelists', pricelists),
    path('pricelist/<int:pl_id>', pricelist),
    path('files', files),
    path('files/folder/<int:folder_id>', folder),

    path('files/doc/create/without', create_doc_without),
    path('files/folder/create/without', create_folder_without),

    path('files/doc/create/<int:fid>', create_doc_on_folder),
    path('files/folder/create/<int:fid>', create_folder_on_folder),
]
