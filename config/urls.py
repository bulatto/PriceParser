from django.contrib import admin
from django.urls import path

import user
import parsing.views
import product.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', parsing.views.index),
    path('show_goods', product.views.show_goods),
    path('add_ref_link', product.views.add_ref_link),
    path('delete_link/<int:product_id>/', product.views.delete_link),
    path('add_ref', product.views.add_ref),
    path('price_task/<int:product_id>/', parsing.views.price_task),
    # path('authentificate', user.views.authentificate)
]
