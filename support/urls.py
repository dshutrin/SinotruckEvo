from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('update_price_list', update_price_list),
    path('pricelist', pricelist)
]
