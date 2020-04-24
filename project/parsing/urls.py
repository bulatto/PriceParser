from django.urls import path

from . import views

app_name = 'parsing'
urlpatterns = [
    path('price_task/<int:product_id>/', views.price_task, name='price_task'),
]
