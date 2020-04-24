from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .helpers import run_price_task

from .helpers import run_price_task


def price_task(request, product_id):
    run_price_task(product_id)
    return redirect(reverse('product:show_goods'))
