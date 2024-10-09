from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('update_price_list', update_price_list),
    path('pricelist', pricelist),
    path('files', files),
    path('files/folder/<int:folder_id>', folder)
]
