from django.contrib import admin
from django.urls import path, include
from config.settings.dev import DEBUG

import user
import parsing.views
import product.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', parsing.views.index),
    path('show_goods', product.views.show_goods),
    path('add_ref_link', product.views.add_product),
    path('delete_link/<int:product_id>/', product.views.delete_product),
    path('add_ref', product.views.add_url_view),
    path('price_task/<int:product_id>/', parsing.views.price_task),
    # path('authentificate', user.views.authentificate)
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]