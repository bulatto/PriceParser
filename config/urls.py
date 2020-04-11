from django.contrib import admin
from django.urls import path

import user.views
import parsing.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', parsing.views.index),
    path('show_goods', parsing.views.show_goods),
    path('add_ref_link', parsing.views.add_ref_link),
    path('delete_link/<int:site_id>/', parsing.views.delete_link),
    path('add_ref', parsing.views.add_ref),
    path('price_task/<int:site_id>/', parsing.views.price_task),
    # path('authentificate', user.views.authentificate)
]
