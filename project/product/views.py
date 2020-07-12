from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from common.helpers import pagination_page
from product.models import Product
from .forms import UrlForm
from .helpers import add_url, GOODS_ON_PAGE
from .helpers import delete_site
from .helpers import get_sites_and_url_form


def show_goods(request, *args, **kwargs):
    products_query = Product.products_with_prices.filter(user=request.user)
    products = pagination_page(
        products_query, request.GET.get('page'), GOODS_ON_PAGE)
    data = get_sites_and_url_form(products)
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
