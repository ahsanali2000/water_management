from django.shortcuts import render, redirect
import datetime
from customer.views import get_product_quantity_map
from database.models import Order, Customer, Area, Vehicle, Schedule, Employee, Bottles
from django.http import HttpResponseNotFound
from customer.views import product_quantity_list


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


def view_order(request, order_id, day=None):
    order = Order.objects.get(id=order_id)
    if request.POST.get('amount_received'):
        messages = ''
        amount_received = int(request.POST.get('amount_received'))
        bottles_given = int(request.POST.get('bottles_given'))
        bottles_received = int(request.POST.get('bottles_received'))
        employee = Employee.objects.get(username=request.user.username)

        if int(order.customer.NoOfBottles) + bottles_given - bottles_received < 0:
            messages = "Invalid No Of bottles"
        elif int(order.price) - amount_received > 0:
            messages = "Invalid Payment entered!"

        else:
            if order.frequency == '1':
                day_ = Schedule.objects.filter(orders=order).distinct().first()
                day_.orders.remove(order)
                day_.day_capacity += order.get_weight()
                day_.save()

            bottle=Bottles.objects.get(id=1)
            bottle.filled = bottle.filled-bottles_given
            bottle.distributed+=(bottles_given - bottles_received)
            bottle.save()

            order.customer.NoOfBottles += (bottles_given - bottles_received)
            order.customer.AmountDue += abs(int(order.price) - amount_received)
            order.delivered = True
            order.delivered_at = datetime.datetime.now()
            order.delivered_by = employee
            order.customer.save()
            order.save()

            employee.receivedBottle += bottles_received
            employee.receivedAmount += amount_received
            employee.save()

            return redirect('areawise_orders', order.vehicle.registrationNo, day, order.area.id)

        return render(request, 'employee/order_delivery_details.html', context={'messages': messages})

    if request.POST and request.user.is_employee and request.user.is_authenticated:
        return render(request, 'employee/order_delivery_details.html')
    elif request.user.is_authenticated and request.user.is_employee:
        customer = order.customer
        data = {'order': order, 'quantity': product_quantity_list(order.desc.all()), 'customer': customer}
        return render(request, 'employee/ordered.html', data)

    return HttpResponseNotFound()


def areawise_orders(request, regNo, areaId, day):
    if request.user.is_authenticated and request.user.is_employee:
        vehicle = Vehicle.objects.get(registrationNo=regNo)
        area = Area.objects.get(id=areaId)
        schedule = Schedule.objects.get(vehicle=vehicle, day=day)
        regular_orders = schedule.orders.filter(frequency='2', area=area, delivered=False)
        one_time_orders = schedule.orders.filter(frequency='1', area=area, delivered=False)
        if regular_orders.first() is None and one_time_orders.first() is None:
            data = {'message': 'No orders found', 'user': Employee.objects.get(username=request.user.username)}
        else:
            data = {'regular_orders': regular_orders, 'one_time_orders': one_time_orders,
                    'user': Employee.objects.get(username=request.user.username), 'day': day}
        return render(request, 'employee/areawise_orders.html', data)
    return HttpResponseNotFound()


def delivered_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(delivered=True)
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
            'orders': orders,
            'massege': "Orders not confirmed",
            'error': error,
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
            'error': error,
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
