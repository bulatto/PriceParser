from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .helpers import (add_message_to_context, get_sites_and_url_form,
                      add_link, delete_site, run_price_task)
from . import forms


def index(request):
    return render(request, 'index.html')


def show_goods(request, *args, **kwargs):
    data = get_sites_and_url_form()
    return render(request, 'show_goods.html', context=data)


def add_ref(request):
    data = {'form': forms.LinkForm()}
    return render(request, 'add_ref.html', context=data)


def add_ref_link(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        message = add_link(url)
        return redirect('/show_goods')


def delete_link(request, site_id):
    if request.method == 'POST':
        message = delete_site(site_id)
        return redirect('/show_goods')


def price_task(request, site_id):
    run_price_task(site_id)
    return redirect('/show_goods')
