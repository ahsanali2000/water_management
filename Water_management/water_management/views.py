from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html',)


def change_password(request):
    if request.user.is_authenticated:
        context = {}
        if request.POST:
            old=request.POST.get('old')
            new1=request.POST.get('new1')
            new2=request.POST.get('new2')
            user = authenticate(username=request.user.username, password=old)
            if not user:
                context['error']='Old password is not correct.'
            elif old==new1:
                context['error']='Old and new passwords can not be same.'
            elif new1!=new2:
                context['error']='New passwords are not matching.'

            if user and new1==new2:
                print('in all')
                user.set_password(new1)
                user.save()
                login(request,user)
                context['message']='Passowrd Changed Sucessfully!'

        return render(request,'change_password.html',context=context)





def check(request):
    return render(request, 'checking.html')
