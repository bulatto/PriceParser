from django.shortcuts import render, redirect

from .forms import UrlForm
from .helpers import get_sites_and_url_form, add_url, delete_site


def show_goods(request, *args, **kwargs):
    data = get_sites_and_url_form()
    return render(request, 'show_goods.html', context=data)


def add_url_view(request):
    data = {'form': UrlForm()}
    return render(request, 'add_url.html', context=data)


def add_product(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        message = add_url(url)
        return redirect('/show_goods')


def delete_product(request, product_id):
    if request.method == 'POST':
        message = delete_site(product_id)
        return redirect('/show_goods')
