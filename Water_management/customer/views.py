from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from database.models import Products, Order, Customer
from ast import literal_eval

def home(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'orders': Order.objects.filter(customer=request.user, delivered=False),
            'massege': "My orders"
        }
        if request.user.is_customer:
            return render(request, 'home.html', context)
    return HttpResponseNotFound()



def view_order(request, order_id):
    order_show = Order.objects.filter(id=order_id).first()
    user_ordered = order_show.customer


    if request.POST and ( request.user.is_superuser or request.user.is_employee):
        delivered= request.POST.get('delivered')
        if delivered:
            order_show.delivered=True
            order_show.save()
        return redirect("/employee/delivered_orders")

    elif request.user.is_authenticated and (request.user.is_superuser or request.user.username == user_ordered.username or request.user.is_employee):
        instance = get_object_or_404(Order, id=order_id)
        address = order_show.address
        frequency = order_show.frequency
        desc = order_show.desc

        splitted = desc.split(',')
        name_list = []
        quan_list = []
        all_list = []
        for pro in splitted:
            further = pro.split(':')  # at ita zeroth index we have product code and at 1st index we have product quantity
            if further[0] != '':
                quan_list.append(further[1])
        product_name = Products.objects.all()
        for a in product_name:
            name_list.append(a.name)
        counter1 = 0
        counter2 = 0
        counter = 1
        for ele in range(2 * len(quan_list)):
            if counter % 2 != 0:
                all_list.append(name_list[counter1])
                counter1 = counter1 + 1
            else:
                all_list.append(quan_list[counter2])
                counter2 = counter2 + 1
            counter = counter + 1
        context = {
            'all_list': all_list,
            'address': address,
            'frequency': int(frequency),
            'user': user_ordered,
            'order':order_show,
        }
        return render(request, 'accounts/ordered.html', context=context)

    return HttpResponseNotFound()


def my_orders(request):
    if request.user.is_authenticated and not request.user.is_superuser and request.user.is_customer:
        orders = Order.objects.filter(customer=request.user)
        context = {
            'orders': orders
        }
        return render(request, 'customer/view_orders.html', context=context)
    return HttpResponseNotFound()
def order_confirmed(request):
    if request.POST and request.user.is_authenticated and request.user.is_customer:
        order_str=request.POST.get("order")
        order_dict = literal_eval(order_str)
        desc= order_dict['desc']
        address= order_dict['address']
        frequency= order_dict['frequency']
        customer= Customer.objects.filter(username=order_dict['customer']).first()

        order= Order.objects.create(desc=desc, address=address,frequency=frequency, customer=customer)
        return redirect(order.get_url())
    return HttpResponseNotFound()


def order(request):
    if request.user.is_authenticated and not request.user.is_superuser and request.user.is_customer:
        context = {
            'products': Products.objects.all(),
        }
        if request.POST:
            product = Products.objects.all()
            list_ordered = []
            flag=0
            for pro in product:
                if request.POST.get(f'{pro.code}')!='' and request.POST.get(f'{pro.code}')!='0':
                    flag=1
            if flag==0:
                context['error']='Kindly add at least one item to order'
                return render(request, 'customer/order_form.html', context=context)


            for pro in product:
                quantity = request.POST.get(f'{pro.code}')
                list_ordered.append( f'{pro.name} : {quantity},')


            desc = ''
            for pro in product:
                quantity = request.POST.get(f'{pro.code}')
                desc = desc + f'{pro.code}:{quantity},'

            address = request.POST.get('address')
            if not address:
                address = request.user.address
            username = request.user.username
            user = Customer.objects.filter(username=username).first()

            frequency = request.POST.get('selected')
            order_dict={'frequency':frequency, 'customer':str(user), 'desc':desc, 'address':address}


            context={
                'order':order_dict,
                'list' : list_ordered,
                'address' : address
            }
            return render(request,'customer/confirm_order.html', context=context)
            # order = Order.objects.create(frequency=frequency, customer=user, desc=desc, address=address)
            # url = order.get_url()
            # return redirect(url)

        return render(request, 'customer/order_form.html', context=context)
    return HttpResponse(status=404)
