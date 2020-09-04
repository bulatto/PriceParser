from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from parsing.tasks import run_celery_price_task

from .helpers import run_price_task


def index(request):
    return render(request, 'index.html')


def price_task(request, product_id):
    run_celery_price_task.delay(product_id)
    return redirect(reverse('product:show_goods'))
