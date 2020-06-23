from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from database.models import Asset,Customer
from Admin.forms import PersonSearchForm
from Admin.views import string_to_list
from .forms import AddAssetForm



def customer_inventory(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user = Customer.objects.filter(is_approved=True)
        if request.POST:
            form = PersonSearchForm(request.POST)
            if form.is_valid():
                try:
                    user = user.filter(id=int(form.cleaned_data['name']))
                except:
                    user = user.filter(name__contains=form.cleaned_data['name'])
            context = {'users': user, 'admin': request.user, 'form': form}
            return render(request, 'inventory/all-customers-inventory.html', context=context)
        context = {'users': user, 'admin': request.user, 'form': PersonSearchForm()}
        return render(request, 'inventory/all-customer-inventory.html', context=context)
    return HttpResponseNotFound()

def inventory_details(request, username=None, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_superuser:
        customer = Customer.objects.get(username=username)
        assets = Asset.objects.all()
        if request.POST:
            asset_string=''
            counter=1
            for item in assets:
                quan = request.POST.get(item.code)
                asset_string += f'{item.code}:{quan}'
                if counter<len(assets):
                    asset_string += ','
                    counter+=1
            customer.assets=asset_string
            customer.save()
            return redirect('/inventory/customer-inventory/')

        product_list = string_to_list(customer.assets)
        assets = Asset.objects.all()
        for product_in_order in product_list:
            for product in assets:
                if product_in_order[0] == product.code:
                    product_in_order[0] = product.code
                    break
        assets_list=[]
        for asset in assets:
            asset.total_amount=0
            for pro in product_list:
                if asset.code == pro[0]:
                    asset.total_amount=int(pro[1])
            assets_list.append(asset)


        return render(request, 'inventory/customer-inventory.html', {'customer':customer, 'assets':assets_list})
    return HttpResponseNotFound()

def all_inventory(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            code = request.POST.get('delete')
            asset=Asset.objects.get(code=code)
            asset.delete()

        assets = Asset.objects.all()
        customers= Customer.objects.filter(is_approved=True)

        available=[]
        given=[]
        total=[]
        for code in assets:
            given.append([code.code, 0])
            available.append([code.code, 0])
            total.append([code.code, code.total_amount])

        for customer in customers:
            product_list = string_to_list(customer.assets)
            for product_in_order in product_list:
                for product in assets:
                    if product_in_order[0] == product.code:
                        product_in_order[0] = product.code
                        break
                counter=0
                for item in product_list:
                    for asset in assets:
                        if asset.code == item[0]:
                            given[counter][1]+= int(item[1])

                    counter+=1
        counter=0
        for item in given:
            for asset in assets:
                if asset.code == item[0]:
                    available[counter][1] = asset.total_amount - int(item[1])

            counter += 1
        in_format=[]
        counter=0
        for asset in assets:
            in_format.append([asset.name, asset.code, available[counter][1], given[counter][1], total[counter][1]])
            in_format.append(asset.code)
            counter+=1
        return render(request, 'inventory/inventory_all.html', {'data':in_format})



def add_asset(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context={}
        if request.POST:
            form = AddAssetForm(request.POST)
            if form.is_valid():
                form.save()
                context['massege'] = 'Asset Added'
            else:
                context['error'] = 'Invalid Input'
        context['form']=AddAssetForm

        return render(request, 'inventory/add_asset.html', context=context)
