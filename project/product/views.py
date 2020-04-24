from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UrlForm
from .helpers import add_url
from .helpers import delete_site
from .helpers import get_sites_and_url_form


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
        return redirect(reverse('product:show_goods'))


def delete_product(request, product_id):
    if request.method == 'POST':
        message = delete_site(product_id)
        return redirect(reverse('product:show_goods'))
