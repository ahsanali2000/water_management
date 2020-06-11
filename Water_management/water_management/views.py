from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.
def home(request):
    context={
        'user':request.user
    }
    if request.user.is_authenticated:
        return render(request,'home.html',context)
    else:
        return render(request,'home.html')
def check(request):
    return render(request,'checking.html')