from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import CustomerRegisterForm

from django.conf import settings

base_dir = settings.BASE_DIR


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        context = {}
        if request.POST:
            form = CustomerRegisterForm(request.POST)
            form.ConfirmPassword = request.POST.get('ConfirmPassword')
            print('view clean')
            if form.is_valid():

                form.save()
                return render(request, 'accounts/approval.html')
            else:
                context['form'] = form
        else:
            context['form'] = CustomerRegisterForm
        return render(request, 'accounts/register.html', context)


def login_user(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['pass']
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_available:
                    if user.is_approved:
                        login(request, user)

                        return redirect('/home/')
                    else:
                        return render(request, 'accounts/approval.html')
                else:

                    HttpResponseNotFound(status=404)

            else:
                context['error'] = 'Invalid Credentials'
                return render(request, 'accounts/login.html', context)
        else:
            return render(request, 'accounts/login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/home/')
    else:
        return HttpResponseNotFound(status=404)
