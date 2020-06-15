from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .forms import CustomerRegisterForm
from .models import Person,Customer
from django.conf import settings
base_dir = settings.BASE_DIR

def details_view(request, username=None,*args,**kwargs):

    if request.POST:
        print('post')
        selection=request.POST.get('selected')
        print(selection)
        if selection=="1":
            user=Customer.objects.filter(username=username)
            user.update(is_approved=True, is_available=True)
            return redirect('/home/')
        if selection=="2":
            user=Customer.objects.filter(username=username)
            user.update(is_approved=False,is_available=True)
            return redirect('/home/')
        if selection=="3":
            user=Customer.objects.filter(username=username)
            user.update(is_available=False)
            return redirect('/home/')


        return redirect('/home/')
    elif request.user.is_authenticated and  (request.user.is_superuser or request.user.username==username):
        instance=get_object_or_404(Customer, username=username)
        context={
            'user':instance
        }
        return render(request, 'accounts/profile.html',context=context)
    return HttpResponseNotFound()
def list_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user=Customer.objects.filter(is_approved=True, is_available=True)
        context={
            'users':user,
            'admin':request.user
        }
        return render(request,'accounts/all-customers.html',context=context)
    return HttpResponseNotFound()
def account_requests(request):
    if request.POST:
        pass
    if request.user.is_authenticated and request.user.is_superuser:
        users= Person.objects.filter(is_approved=False)
        print(users)
        context={
            'users':users,
            'requesting':request.user
        }
        return render(request,'accounts/requests.html',context)
    return HttpResponseNotFound()

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        context = {}
        if request.POST:
            form = CustomerRegisterForm(request.POST)
            form.ConfirmPassword=request.POST.get('ConfirmPassword')
            print('view clean')
            if form.is_valid():

                form.save()
                return render(request,'accounts/approval.html')
            else:
                context['form'] = form
        else:
            context['form']=CustomerRegisterForm
        return render(request,'accounts/register.html',context)




def login_user(request):
    context={}
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            users=Person.objects.all()
            password = request.POST['pass']
            user = authenticate(request,username=username,password=password)
            print(user)

            if user:
                if user.is_available:
                    if user.is_approved :
                        login(request, user)

                        return redirect('/home/')
                    else:
                        return render(request,'accounts/approval.html')
                else:
                    return HttpResponseNotFound()

            else:
                context['error'] = 'Invalid Credentials'
                return render(request,'accounts/login.html',context)

        return render(request,'accounts/login.html')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/home/')
    else:
        return HttpResponseNotFound(status=404)