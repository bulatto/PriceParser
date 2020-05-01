from django.shortcuts import render
from django.http import HttpResponse

from .helpers import auth


def login(request):
    data = {'is_try_again': False}
    return render(request, 'login.html', context=data)


def authentificate(request):
    login = request.POST.get('login')
    password = request.POST.get('password')
    is_correct, message = auth(login, password)
    if is_correct:
        return HttpResponse(f'Вы успешно авторизированы ({message}')
    else:
        data = {'is_try_again': True}
        return render(request, 'login.html', context=data)



