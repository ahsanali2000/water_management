from django.shortcuts import render
from database.models import Person, Customer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound


def details_view(request, username=None, *args, **kwargs):
    if request.POST and request.user.is_superuser:
        selection = request.POST.get('selected')
        NoOfBottles = request.POST.get('NoOfBottles')
        MonthlyBill = request.POST.get('MonthlyBill')
        AmountDue = request.POST.get('AmountDue')
        user = Customer.objects.filter(username=username)
        if selection == "1":
            user.update(is_approved=True, is_available=True)
            return redirect('/home/')
        if selection == "2":
            user.update(is_approved=False)
            return redirect('/home/')
        if selection == "3":
            user.update(is_available=False, is_approved=False)
            return redirect('/home/')
        user.update(NoOfBottles=NoOfBottles,MonthlyBill=MonthlyBill,AmountDue=AmountDue)
        return redirect('/home/')

        #customer ki info edit kro
        return redirect('/home/')
    elif request.user.is_authenticated and (request.user.is_superuser or request.user.username == username):
        instance = get_object_or_404(Person,username=username)
        if instance.is_customer :
            instance= get_object_or_404(Customer, username=username)
        context = {
            'user': instance
        }
        return render(request, 'accounts/profile.html', context=context)
    return HttpResponseNotFound()


def list_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user = Customer.objects.filter(is_approved=True)
        context = {
            'users': user,
            'admin': request.user
        }
        return render(request, 'accounts/all-customers.html', context=context)
    return HttpResponseNotFound()


def account_requests(request):
    if request.POST:
        pass
    if request.user.is_authenticated and request.user.is_superuser:
        users = Person.objects.filter(is_approved=False)
        users = users.exclude(is_admin=True)
        print(users)
        context = {
            'users': users,
            'requesting': request.user
        }
        return render(request, 'accounts/requests.html', context)
    return HttpResponseNotFound()
