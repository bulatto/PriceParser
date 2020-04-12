from django.shortcuts import render, redirect

from .helpers import (run_price_task)


def index(request):
    return render(request, 'index.html')


def price_task(request, product_id):
    run_price_task(product_id)
    return redirect('/show_goods')
