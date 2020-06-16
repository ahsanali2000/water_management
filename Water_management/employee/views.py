from django.shortcuts import render
from database.models import Order
from django.http import HttpResponseNotFound




def delivered_orders(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'orders': Order.objects.filter(delivered=True),
            'massege': "Delivered orders"
        }
        if request.user.is_employee or request.user.is_superuser:
            return render(request, 'employee/order_list.html', context)
    return HttpResponseNotFound()
def not_confirmed(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'orders': Order.objects.filter(confirmed=False),
            'massege': "Orders not confirmed"
        }
        if request.user.is_employee or request.user.is_superuser:
            return render(request, 'employee/order_list.html', context)
    return HttpResponseNotFound()
def confirmed_not_delivered_orders(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'orders': Order.objects.filter(delivered=False, confirmed=True),
            'massege': 'Confirm orders'
        }
        if request.user.is_employee or request.user.is_superuser:
            return render(request, 'employee/order_list.html', context)
    return HttpResponseNotFound()
def home(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'orders': Order.objects.filter(delivered=False),
            'massege': "Orders"
        }
        if request.user.is_employee:
            return render(request, 'home.html', context)
    return render(request, 'home.html')