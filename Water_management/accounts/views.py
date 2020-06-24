from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from database.models import Area,Customer
from .forms import CustomerRegisterForm, CorporateRegisterForm


from django.conf import settings
base_dir = settings.BASE_DIR


def register_user(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/home/')
        elif request.user.is_customer:
            return redirect('/customer/home/')
        elif request.user.is_employee:
            return redirect('/employee/home')
    else:
        context = {}
        if request.POST:
            form = CustomerRegisterForm(request.POST)
            form.ConfirmPassword = request.POST.get('ConfirmPassword')
            if form.is_valid():
                form.save()
                if 'not'==request.POST.get('selected_area'):
                    user= Customer.objects.get(username=form.cleaned_data.get('username'))
                    user.NotInArea=True
                    user.save()
                    return render(request, 'accounts/approval.html',{'user':user})
                return render(request, 'accounts/approval.html')
            else:
                context['form'] = form
                context['areas'] = Area.objects.all()
        else:
            context['form'] = CustomerRegisterForm
            context['areas'] = Area.objects.all()
        return render(request, 'accounts/register.html', context)

def  register_corporate(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/home/')
        elif request.user.is_customer:
            return redirect('/customer/home/')
        elif request.user.is_employee:
            return redirect('/employee/home')
    else:
        context = {}
        if request.POST:
            form = CorporateRegisterForm(request.POST)
            form.ConfirmPassword = request.POST.get('ConfirmPassword')
            if form.is_valid():
                form.save()
                if 'not'==request.POST.get('selected_area'):
                    user= Customer.objects.get(username=form.cleaned_data.get('username'))
                    user.NotInArea=True
                    user.save()
                    return render(request, 'accounts/approval.html',{'user':user})
                return render(request, 'accounts/approval.html')
            else:
                context['form'] = form
                context['areas'] = Area.objects.all()
        else:
            context['form'] = CorporateRegisterForm
            context['areas'] = Area.objects.all()
        return render(request, 'accounts/register_corporate.html', context)

def login_user(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/home/')
        elif request.user.is_customer:
            return redirect('/customer/home/')
        elif request.user.is_employee:
            return redirect('/employee/home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['pass']
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_available:
                    if user.is_approved:
                        login(request, user)
                        if user.is_customer:
                            return redirect('/customer/home/')
                        if user.is_employee:
                            return redirect('/employee/home/')
                        if user.is_superuser:
                            return redirect('/admin/home/')
                    else:
                        return render(request, 'accounts/approval.html',{'user': Customer.objects.get(username=user.username)})
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
