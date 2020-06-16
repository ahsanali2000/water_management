from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html',)


def edit_profile(request):
    if request.user.is_authenticated:
        context = {}
        if request.POST:
            name=request.POST.get('name')
            email=request.POST.get('email')
            cnic=request.POST.get('cnic')
            PhoneNo=request.POST.get('PhoneNo')
            User=request.user
            if name != request.user.name or cnic != request.user.cnic or email != request.user.email or PhoneNo != request.user.PhoneNo:
                if name != request.user.name:
                    User.name=name
                if cnic != request.user.cnic:
                    User.cnic=cnic
                if email != request.user.email:
                    User.email=email
                if PhoneNo != request.user.PhoneNo:
                    User.PhoneNo=PhoneNo
                context['message'] = 'Profile Updated successfully!'
                User.save()
            else:
                context['message']='No change detected'


            old=request.POST.get('old')
            new1=request.POST.get('new1')
            new2=request.POST.get('new2')
            if (old and new2 and new1):
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

        return render(request, 'edit_profile.html', context=context)





def check(request):
    return render(request, 'checking.html')
