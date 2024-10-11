from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('pricelists', pricelists),
    path('update_price_list/<int:pl_id>', update_price_list),
    path('pricelist/create', create_pricelist),
    path('pricelist/<int:pl_id>/delete', delete_pricelist),
    path('pricelist/<int:pl_id>', pricelist),

    path('files', files),
    path('files/folder/<int:folder_id>', folder),
    path('files/doc/create/without', create_doc_without),
    path('files/folder/create/without', create_folder_without),
    path('files/doc/create/<int:fid>', create_doc_on_folder),
    path('files/folder/create/<int:fid>', create_folder_on_folder),
    path('remove_document', remove_document),
    path('remove_folder', remove_folder),

    path('activitys', activitys),
    path('activitys/user/<int:uid>', user_activity),
    path('activitys/user/<int:uid>/download', download_user_activity),

    path('contacts', contacts),
    path('users/<int:uid>/edit', edit_user),
    path('users/add', add_user),

    path('login', login_view),
    path('logout', logout_view)
]
