from django.urls import path

from . import views

app_name = 'product'
urlpatterns = [
    path('show_goods', views.show_goods, name='show_goods'),
    path('add_product_url', views.add_product, name='add_product_url'),
    path('delete_product/<int:product_id>/', views.delete_product,
         name='delete_product'),
    path('add_ref', views.add_url_view, name='add_ref'),
]