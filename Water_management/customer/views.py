from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from database.models import Products, Order, Customer
from ast import literal_eval
from .forms import OrderForm, OrderQuantityForm
from Admin.views import string_to_list, form_to_string

order = None


def home(request):
    context = {
        'user': Customer.objects.get(username=request.user.username),
        'orders': Order.objects.filter(customer=request.user, delivered=False)
    }
    if request.user.is_authenticated:
        return render(request, 'customer/home.html', context)
    else:
        return render(request, 'home.html')


def view_order(request, order_id):
    if request.user.is_authenticated and not request.user.is_superuser:
        order = Order.objects.get(id=order_id)
        customer = order.customer
        data = {'order': order, 'quantity': get_product_quantity_map(order.desc), 'customer': customer}
        return render(request, 'customer/ordered.html', data)

    return HttpResponseNotFound()


def my_orders(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        orders = Order.objects.filter(customer=request.user).order_by('-ordered_at')
        context = {
            'orders': orders,
            'user': Customer.objects.get(username=request.user.username)
        }
        return render(request, 'customer/view_orders.html', context=context)


def order_confirmed(request):
    if request.POST and request.user.is_authenticated:
        global order
        order.save()
        print(order)
        order = None
        return redirect('customer_home')
    return HttpResponseNotFound()


def order(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.POST:
            global order
            orderForm = OrderForm(request.POST)
            customer = Customer.objects.get(username=request.user.username)
            quantityForm = OrderQuantityForm(request.POST)
            if orderForm.is_valid() and quantityForm.is_valid():
                quantity = form_to_string(quantityForm)
                if not has_quantity(quantity):
                    return render(request, 'customer/order_form.html',
                                  {'message': 'Invalid Data or Empty order!', 'order_form': OrderForm(),
                                   'quantity_form': OrderQuantityForm()})
                price = get_price(quantity, customer)
                order = Order(desc=quantity, customer=customer, frequency=orderForm.cleaned_data['order_type'],
                              address=orderForm.cleaned_data['address'] if orderForm.cleaned_data[
                                  'address'] else customer.address, price=price)
                data = {'order': order, 'quantity': get_product_quantity_map(order.desc), 'customer': customer,
                        'price': price}
                return render(request, 'customer/confirm_order.html', data)
            return render(request, 'customer/order_form.html',
                          {'message': 'Please retry!', 'order_form': OrderForm(), 'quantity_form': OrderQuantityForm()})
        return render(request, 'customer/order_form.html',
                      {'order_form': OrderForm(), 'quantity_form': OrderQuantityForm()})
    return HttpResponse(status=404)


def get_price(description, customer):
    prices = string_to_list(customer.discounted_price)
    products = string_to_list(description)
    net_price = 0
    for product in products:
        for price in prices:
            if product[0] == price[0]:
                net_price += int(price[1]) * int(product[1])
                break
    return net_price


def get_product_quantity_map(description):
    product_list = string_to_list(description)
    products = Products.objects.all()
    for product_in_order in product_list:
        for product in products:
            if product_in_order[0] == product.code:
                product_in_order[0] = product.name
                break
    return product_list


def has_quantity(description):
    products = string_to_list(description)
    valid = False
    for product in products:
        if int(product[1]) < 0:
            return False
        if int(product[1]) > 0:
            valid = True
    return valid


def profile(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(username=request.user.username)
        if customer:
            data = {'user': customer}
            return render(request, 'customer/profile.html', data)
    return HttpResponseNotFound()
