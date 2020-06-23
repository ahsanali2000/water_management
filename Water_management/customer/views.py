from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from database.models import Products, Order, Customer, Area, Asset
from ast import literal_eval
from .forms import OrderForm, OrderQuantityForm
from Admin.views import string_to_list, form_to_string

order = None


def home(request):
    user=Customer.objects.get(username=request.user.username)


    product_list = string_to_list(user.assets)
    products = Asset.objects.all()
    for product_in_order in product_list:
        for product in products:
            if product_in_order[0] == product.code:
                product_in_order[0] = product.name
                break
    context = {
        'user': user,
        'assets':product_list,
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
        user = Customer.objects.get(username=request.user.username)

        product_list = string_to_list(user.assets)
        products = Asset.objects.all()
        for product_in_order in product_list:
            for product in products:
                if product_in_order[0] == product.code:
                    product_in_order[0] = product.name
                    break

        orders = Order.objects.filter(customer=request.user).order_by('-ordered_at')
        context = {
            'orders': orders,
            'user': user,
            'assets':product_list
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
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_employee:
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



                if orderForm.cleaned_data.get('address') and request.POST.get('selected_area'):
                    address = orderForm.cleaned_data.get('address')
                    selected_area =Area.objects.get(id=int( request.POST.get('selected_area')))
                else:
                    address = customer.address
                    selected_area = customer.area

                order = Order(desc=quantity, customer=customer, frequency=orderForm.cleaned_data['order_type'],
                              address=address, area=selected_area , price=price)
                data = {'order': order, 'quantity': get_product_quantity_map(order.desc), 'customer': customer,
                        'price': price}
                return render(request, 'customer/confirm_order.html', data)
            return render(request, 'customer/order_form.html',
                          {'message': 'Please retry!', 'order_form': OrderForm(), 'quantity_form': OrderQuantityForm()})
        return render(request, 'customer/order_form.html',
                      {
                          'order_form': OrderForm(),
                          'quantity_form': OrderQuantityForm(),
                          'areas'   : Area.objects.all(),

                       })
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
        user = Customer.objects.get(username=request.user.username)

        product_list = string_to_list(user.assets)
        products = Asset.objects.all()
        for product_in_order in product_list:
            for product in products:
                if product_in_order[0] == product.code:
                    product_in_order[0] = product.name
                    break
        if user:
            data = {'user': user,'assets':product_list}
            return render(request, 'customer/profile.html', data)
    return HttpResponseNotFound()
