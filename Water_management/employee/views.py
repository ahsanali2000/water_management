from django.shortcuts import render, redirect
import datetime
from customer.views import get_product_quantity_map
from Admin.views import string_to_list
from database.models import Order, Customer, Area, Vehicle, Schedule, Employee,Asset
from django.http import HttpResponseNotFound


def employee_schedule(request, regNo):
    if request.user.is_authenticated and request.user.is_employee:
        vehicle = Vehicle.objects.get(registrationNo=regNo)
        schedule = Schedule.objects.filter(vehicle=vehicle).order_by('order')
        data = {'schedule': schedule, "user": Employee.objects.get(username=request.user.username), 'regNo': regNo}
        return render(request, 'employee/schedule.html', data)
    return HttpResponseNotFound()


def show_schedule(request):
    if request.user.is_authenticated and request.user.is_employee:
        vehicles = Vehicle.objects.filter(employee=request.user)
        data = {'vehicles': vehicles, "user": Employee.objects.get(username=request.user.username)}
        return render(request, 'employee/selectVehicle.html', context=data)
    return HttpResponseNotFound()



def view_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.POST.get('amount_received'):
        messages =''
        amount_received = int(request.POST.get('amount_received'))
        bottles_given = int(request.POST.get('bottles_given'))
        bottles_received = int(request.POST.get('bottles_received'))
        employee = Employee.objects.get(username=request.user.username)

        product_list = string_to_list(order.customer.assets)
        products = Asset.objects.all()
        for product_in_order in product_list:
            for product in products:
                if product_in_order[0] == product.code:
                    product_in_order[0] = product.code
                    break
        NoOfBottles = int(product_list[0][1])

        if int(NoOfBottles) + bottles_given - bottles_received < 0:
            messages = "Invalid No Of bottles"
        elif int(order.customer.AmountDue) + int(order.price) - amount_received < 0:
            messages = "Invalid Payment entered!"

        else:

            NoOfBottles += (bottles_given - bottles_received)
            assets=""
            product_list[0][1] = NoOfBottles
            counter=1
            for pair in product_list:
                assets += str(pair[0]) + ":" + str(pair[1])
                if counter < len(product_list):
                    assets += ","
                counter+=1
            customer=order.customer

            customer.assets=assets
            customer.AmountDue += (int(order.price) - amount_received)
            customer.save()

            order.delivered = True
            order.delivered_at = datetime.datetime.now()
            order.save()


            employee.receivedBottle += bottles_received
            employee.receivedAmount += amount_received
            employee.save()

            return redirect('areawise_orders', order.vehicle.registrationNo, order.area.id)

        return render(request, 'employee/order_delivery_details.html',context={ 'messages' : messages })

    if request.POST and request.user.is_employee and request.user.is_authenticated:
        return render(request, 'employee/order_delivery_details.html')
    elif request.user.is_authenticated and request.user.is_employee:
        customer = order.customer
        data = {'order': order, 'quantity': get_product_quantity_map(order.desc), 'customer': customer}
        return render(request, 'employee/ordered.html', data)

    return HttpResponseNotFound()



def areawise_orders(request, regNo, areaId):
    if request.user.is_authenticated and request.user.is_employee:
        vehicle = Vehicle.objects.get(registrationNo=regNo)
        area = Area.objects.get(id=areaId)
        regular_orders = Order.objects.filter(vehicle=vehicle, area=area, delivered=False, frequency='2')
        one_time_orders = Order.objects.filter(vehicle=vehicle, area=area, delivered=False, frequency='1')
        if regular_orders.first() is None and one_time_orders.first() is None:
            data = {'message': 'No orders found', 'user': Employee.objects.get(username=request.user.username)}
        else:
            data = {'regular_orders': regular_orders, 'one_time_orders': one_time_orders,
                    'user': Employee.objects.get(username=request.user.username)}
        return render(request, 'employee/areawise_orders.html', data)
    return HttpResponseNotFound()


def delivered_orders(request):
    if request.user.is_authenticated:
        orders=Order.objects.filter(delivered=True)
        error = None
        if not orders:
            error = 'No order found'
        context = {
            'user': Employee.objects.get(username=request.user.username),
            'orders': orders,
            'error': error,
            'massege': "Delivered orders"
        }
        if request.user.is_employee or request.user.is_superuser:
            return render(request, 'employee/order_list.html', context)
    return HttpResponseNotFound()


def not_confirmed(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(confirmed=False)
        error = None
        if not orders.first():
            error = "No order found"
        context = {
            'user': Employee.objects.get(username=request.user.username),
            'orders': orders ,
            'massege': "Orders not confirmed",
            'error' : error ,
        }
        if request.user.is_employee or request.user.is_superuser:
            return render(request, 'employee/order_list.html', context)
    return HttpResponseNotFound()


def confirmed_not_delivered_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(delivered=False, confirmed=True)
        error = None
        if not orders:
            error = 'No order found'
        context = {
            'user': Employee.objects.get(username=request.user.username),
            'orders': orders,
            'error':error,
            'massege': 'Confirm orders'
        }
        if request.user.is_employee or request.user.is_superuser:
            return render(request, 'employee/order_list.html', context)
    return HttpResponseNotFound()


def home(request):
    if request.user.is_authenticated:
        context = {
            'user': Employee.objects.get(username=request.user.username),
            'orders': Order.objects.filter(delivered=False),
            'massege': "Orders"
        }
        if request.user.is_employee:
            return render(request, 'employee/home.html', context)
    return render(request, 'home.html')


def profile(request):
    if request.user.is_authenticated:
        data = {'user': Employee.objects.get(username=request.user.username)}
        return render(request, 'employee/profile.html', data)
    return HttpResponseNotFound()
