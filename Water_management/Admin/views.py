from django.shortcuts import render
from database.models import Person, Customer, Order, City, Area, Vehicle, Schedule, Products, Employee
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .forms import EmployeeCreateForm, VehicleCreateForm, AreaCreateForm, \
    CityCreateForm, EmployeeEditForm, VehicleEditForm, SearchOrdersForm, PersonSearchForm, VehicleSearchForm, \
    ConfirmOrderForm, SelectAreaOfOrderForm, CustomerApprovalForm, AddDiscountedPrices, CreateProductForm, \
    EditProductForm
from django.forms import formset_factory, modelformset_factory
from django import forms


def home(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'notifications': get_notifications()
        }
        if request.user.is_superuser:
            return render(request, 'admin/home.html', context)
    return render(request, 'home.html')


def details_view(request, username=None, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_superuser:
        customer = Customer.objects.get(username=username)
        if request.POST:
            customerInfoForm = CustomerApprovalForm(request.POST)
            productInfoForm = AddDiscountedPrices(request.POST)
            if customerInfoForm.is_valid() and productInfoForm.is_valid():
                discounted_prices = form_to_string(productInfoForm)
                customer.discounted_price = discounted_prices
                customer.NoOfBottles = customerInfoForm.cleaned_data['NoOfBottles']
                customer.MonthlyBill = customerInfoForm.cleaned_data['MonthlyBill']
                status = customerInfoForm.cleaned_data['status']
                if status == "1":
                    customer.is_approved = False
                elif status == "2":
                    customer.is_approved = True
                    customer.is_available = True
                elif status == "3":
                    customer.is_approved = False
                    customer.is_available = False
                customer.save()
                return redirect('admin_home')
            data = {'info_form': customerInfoForm, "product_form": productInfoForm, 'customer': customer}
            return render(request, 'admin/approveCustomer.html', data)
        if customer.is_approved and customer.is_available:
            status = 2
        elif not customer.is_available and not customer.is_approved:
            status = 3
        else:
            status = 1
        if customer.discounted_price:
            default_prices = {}
            for pair in string_to_list(customer.discounted_price):
                default_prices[pair[0]] = int(pair[1])
            data = {'info_form': CustomerApprovalForm(
                initial={'NoOfBottles': customer.NoOfBottles, 'MonthlyBill': customer.MonthlyBill,
                         'status': status}), 'customer': customer, 'product_form': AddDiscountedPrices(
                initial=default_prices
            )}
        else:
            data = {'info_form': CustomerApprovalForm(
                initial={'NoOfBottles': customer.NoOfBottles, 'MonthlyBill': customer.MonthlyBill,
                         'status': status}), 'customer': customer, 'product_form': AddDiscountedPrices()}
        return render(request, 'admin/approveCustomer.html', data)
    return HttpResponseNotFound()


def list_view(request):
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
            return render(request, 'admin/all-customers.html', context=context)
        context = {'users': user, 'admin': request.user, 'form': PersonSearchForm()}
        return render(request, 'admin/all-customers.html', context=context)
    return HttpResponseNotFound()


def account_requests(request):
    if request.POST:
        pass
    if request.user.is_authenticated and request.user.is_superuser:
        users = Person.objects.filter(is_approved=False)
        users = users.exclude(is_admin=True)
        users = users.exclude(is_employee=True)
        context = {
            'users': users,
            'requesting': request.user
        }
        return render(request, 'admin/requests.html', context)
    return HttpResponseNotFound()


def add_employee(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = EmployeeCreateForm(request.POST)
            if form.is_valid():
                form.save()
                data = {'message': "Employee Created Successfully!", 'form': EmployeeCreateForm()}
            else:
                data = {'message': "Invalid data entered. Please retry!", 'form': form}
            return render(request, 'admin/newEmployee.html', data)  # Add this Template later
        return render(request, 'admin/newEmployee.html', {'form': EmployeeCreateForm()})
    return HttpResponseNotFound()


def all_employee(request):
    if request.user.is_authenticated and request.user.is_superuser:
        employee = Person.objects.filter(is_employee=True)
        if request.POST:
            form = PersonSearchForm(request.POST)
            if form.is_valid():
                try:
                    employee = employee.filter(id=int(form.cleaned_data['name']))
                except:
                    employee = employee.filter(name__contains=form.cleaned_data['name'])
            data = {'allEmployee': employee, 'admin': request.user, 'form': form}
            return render(request, 'admin/allEmployee.html', data)
        data = {'allEmployee': employee, 'admin': request.user, 'form': PersonSearchForm()}
        return render(request, "admin/allEmployee.html", data)  # Add this Template later
    return HttpResponseNotFound()


def edit_employee(request, username):
    if request.user.is_authenticated and request.user.is_superuser:
        employee = Person.objects.get(username=username)
        if request.POST:
            filled_form = EmployeeEditForm(request.POST, instance=employee)
            if filled_form.is_valid():
                filled_form.save()
        data = {"employee": employee, 'form': EmployeeEditForm(instance=employee)}
        return render(request, "admin/editEmployee.html", data)  # Add this Template later
    return HttpResponseNotFound()


def add_city(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            form = CityCreateForm(request.POST)
            if form.is_valid():
                form.save()
                data = {"message": "City Added Successfully!", "form": CityCreateForm(), 'admin': request.user}
            else:
                data = {"message": "This City Already Exists Please Retry!", "form": form, 'admin': request.user}
            return render(request, 'admin/newCity.html', data)  # Add this template later
        return render(request, 'admin/newCity.html', {'form': CityCreateForm(), 'admin': request.user})
    return HttpResponseNotFound()


def add_area(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            form = AreaCreateForm(request.POST)
            if form.is_valid():
                form.save()
                data = {"message": "Area Added Successfully!", "form": AreaCreateForm()}
            else:
                data = {"message": "Invalid Data Please Retry!", "form": form}
            return render(request, 'admin/newArea.html', data)  # Add this template later
        return render(request, 'admin/newArea.html', {'form': AreaCreateForm()})
    return HttpResponseNotFound()


def all_areas(request, city):
    if request.user.is_authenticated and request.user.is_superuser:
        if city:
            areas = Area.objects.filter(city__city=city)
            data = {"areas": areas, 'requesting': request.user}
            return render(request, "admin/allArea.html", data)  # Add this Template later
    return HttpResponseNotFound()


def all_cities(request):
    if request.user.is_authenticated and request.user.is_superuser:
        cities = City.objects.all()
        data = {"cities": cities, 'requesting': request.user}
        return render(request, "admin/allCities.html", data)  # Add this Template later
    return HttpResponseNotFound()


def add_vehicle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        index = 0
        if request.POST:
            form = VehicleCreateForm(request.POST)
            if form.is_valid():
                if " " not in form.cleaned_data['registrationNo']:
                    vehicle = form.save()
                    for day in week:
                        Schedule(day=day, vehicle=vehicle, order=index).save()
                        index += 1
                    data = {"message": "Vehicle Added Successfully!", "form": VehicleCreateForm()}
                else:
                    data = {
                        "message": "Vehicle registration number must not contain spaces use \"-\" instead like VAR-2345",
                        "form": form}
            else:
                data = {"message": "Invalid Data Please Retry!", "form": form}
            return render(request, 'admin/newVehicle.html', data)  # Add this template later
        return render(request, 'admin/newVehicle.html', {'form': VehicleCreateForm()})
    return HttpResponseNotFound()


def all_vehicle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicles = Vehicle.objects.all()
        if request.POST:
            form = VehicleSearchForm(request.POST)
            if form.is_valid():
                vehicles = vehicles.filter(registrationNo__contains=form.cleaned_data['regNo'])
            print(vehicles)
            data = {'vehicles': vehicles, 'admin': request.user, 'form': form}
            return render(request, 'admin/allVehicle.html', data)
        data = {'vehicles': vehicles, "requesting": request.user, 'form': VehicleSearchForm()}
        return render(request, "admin/allVehicle.html", data)  # Add this Template later
    return HttpResponseNotFound()


def edit_vehicle(request, regNo):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicle = Vehicle.objects.get(registrationNo=regNo)
        if request.POST:
            form = VehicleEditForm(request.POST, instance=vehicle)
            if form.is_valid():
                form.save()
                data = {"message": "Vehicle Updated Successfully!", "form": form, 'vehicle': vehicle,
                        'user': request.user}
            else:
                data = {"message": "Invalid Data Please Retry!", "form": form, 'vehicle': vehicle, 'user': request.user}
            return render(request, 'admin/editVehicle.html', data)  # Add this template later
        data = {'form': VehicleEditForm(instance=vehicle), 'vehicle': vehicle, 'user': request.user}
        return render(request, 'admin/editVehicle.html', data)
    return HttpResponseNotFound()


def update_schedule(request, regNo):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicle = Vehicle.objects.get(registrationNo=regNo)
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        schedule_formset = modelformset_factory(Schedule, fields=['areas'], labels={
            'areas': ''
        }, widgets={
            'areas': forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker',
                    'data-live-search': 'true',
                },
            ),
        }, extra=0, min_num=0, max_num=7)
        query_set = Schedule.objects.filter(vehicle=vehicle).order_by('order')
        if request.POST:
            form_set = schedule_formset(request.POST)
            if form_set.is_valid():
                form_set.save()
                data = {'message': 'Schedule Updated Successfully!', 'formset': form_set, 'week': week}
            else:
                data = {'message': 'Schedule Update Failed!', 'formset': form_set, 'week': week}
            return render(request, 'admin/updateSchedule.html', data)
        formset = schedule_formset(queryset=query_set)
        data = {'formset': formset, 'week': week}
        return render(request, 'admin/updateSchedule.html', data)
    return HttpResponseNotFound()


def show_vehicle_for_schedule(request, page):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicles = Vehicle.objects.all()
        if request.POST:
            form = VehicleSearchForm(request.POST)
            if form.is_valid():
                vehicles = vehicles.filter(registrationNo__contains=form.cleaned_data['regNo'])
            print(vehicles)
            data = {'vehicles': vehicles, 'admin': request.user, 'form': form, 'page': page}
            return render(request, 'admin/selectVehicle.html', data)
        data = {'vehicles': vehicles, "requesting": request.user, 'page': page, 'form': VehicleSearchForm()}
        return render(request, 'admin/selectVehicle.html', data)  # add this template later


def show_vehicle_schedule(request, regNo):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicle = Vehicle.objects.get(registrationNo=regNo)
        schedule = Schedule.objects.filter(vehicle=vehicle)
        schedule = sort_schedule(schedule)
        data = {'schedule': schedule, "user": request.user}
        return render(request, 'admin/schedule.html', data)  # add this template later


def get_notifications():
    notifications = []

    new_customers = Customer.objects.filter(is_approved=False).count()
    notifications.append("{} Customer{} waiting for approval.".format(new_customers, "" if new_customers == 1 else "s"))
    new_orders = Order.objects.filter(confirmed=False).count()
    notifications.append("{} Unconfirmed Order{}".format(new_orders, "" if new_orders == 1 else "s"))
    amount_due = 0
    bottles_reveived = 0
    for employee in Employee.objects.all():
        amount_due += employee.receivedAmount
        bottles_reveived += employee.receivedBottle
    notifications.append('Total amount received : {} Rs'.format(amount_due))
    notifications.append('Total bottles received : {}'.format(bottles_reveived))

    return notifications


def profile(request):
    if request.user.is_authenticated and request.user.is_superuser:
        data = {'user': request.user}
        return render(request, 'admin/profile.html', data)
    return HttpResponseNotFound()


def sort_schedule(schedule):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sorted_data = []
    index = 0
    for i in range(0, 6):
        for single_day in schedule:
            if single_day.day == days[index]:
                sorted_data.append(single_day)
                index += 1
                if index > 6:
                    return sorted_data
    return sorted_data


def search_order(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all().order_by('-ordered_at')
        if request.POST:
            form = SearchOrdersForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                print(status)
                if status == "delivered":
                    orders = orders.filter(delivered=True)
                elif status == 'confirmed':
                    orders = orders.filter(confirmed=True)
                elif status == 'unconfirmed':
                    orders = orders.filter(confirmed=False)
                elif status == "regular":
                    orders = orders.filter(frequency='2')
                elif status == "only once":
                    orders = orders.filter(frequency='1')
                elif status == "confirmed & not delivered":
                    orders = orders.filter(delivered=False, confirmed=True)
                customer = form.cleaned_data['customer_search']
                if customer:
                    try:
                        order_id = int(customer)
                        orders = orders.filter(id=order_id)
                    except:
                        orders = orders.filter(customer__name__contains=customer)
                data = {'user': request.user, 'orders': orders, 'form': form}
                return render(request, 'admin/orders.html', data)
        data = {'user': request.user, 'orders': orders, 'form': SearchOrdersForm()}
        return render(request, 'admin/orders.html', data)
    return HttpResponseNotFound()


def confirm_order(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=int(id))
        if request.POST:
            form = ConfirmOrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('add_vehicle_to_order', id=id)
            data = {'message': 'Invalid Data, Please Retry!', 'form': form, 'order': order}
            return render(request, 'admin/selectArea.html', data)
        data = {'order': order, 'form': ConfirmOrderForm()}
        return render(request, 'admin/selectArea.html', data)
    return HttpResponseNotFound()


def select_vehicle_for_order(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=id)
        if request.POST:
            form = SelectAreaOfOrderForm(request.POST, area=order.area)
            if form.is_valid():
                vehicle = Vehicle.objects.get(registrationNo=form.cleaned_data['vehicle'])
                order.vehicle = vehicle
                order.save()
                return redirect('admin_home')
            data = {'message': 'Invalid Data, Please Retry!', 'form': form}
            return render(request, 'admin/orderVehicle.html', data)
        data = {'order': order, 'form': SelectAreaOfOrderForm(area=order.area)}
        return render(request, 'admin/orderVehicle.html', data)
    return HttpResponseNotFound()


def form_to_string(form):
    string = ""
    for field in form.fields:
        string += "{}:{},".format(field, form.cleaned_data[field])
    string = string[:-1]
    return string


def string_to_list(string_data):
    string = str(string_data).split(',')
    string_list = []
    for pairs in string:
        string_list.append(pairs.split(":"))
    return string_list


def add_product(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            form = CreateProductForm(request.POST)
            if form.is_valid():
                product = form.save()
                for customer in Customer.objects.all():
                    customer.discounted_price += ",{}:{}".format(str(product.code), str(product.price))
                    customer.save()
                data = {'message': 'Product added successfully!', 'form': CreateProductForm(), 'user': request.user}
            else:
                data = {'message': 'Invalid Data, Please Retry!', 'form': form, 'user': request.user}
            return render(request, 'admin/newProduct.html', data)
        data = {'user': request.user, 'form': CreateProductForm()}
        return render(request, 'admin/newProduct.html', data)
    return HttpResponseNotFound()


def edit_product(request, code):
    if request.user.is_authenticated and request.user.is_superuser:
        product = Products.objects.get(code=code)
        if request.POST:
            form = EditProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                data = {'message': 'Product updated successfully!', 'form': form, 'user': request.user,
                        'message_type': 'success'}
            else:
                data = {'message': 'Invalid Data, Please Retry!', 'form': form, 'user': request.user,
                        'message_type': 'failure'}
            return render(request, 'admin/newProduct.html', data)
        data = {'user': request.user, 'form': EditProductForm(instance=product)}
        return render(request, 'admin/newProduct.html', data)
    return HttpResponseNotFound()


def all_products(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Products.objects.all()
        data = {'products': products, 'user': request.user}
        return render(request, 'admin/allProducts.html', data)
    return HttpResponseNotFound()


def show_records(request):
    if request.user.is_authenticated and request.user.is_superuser:
        employees = Employee.objects.all().order_by('receivedAmount')
        employees = employees.exclude(receivedAmount=0)
        if request.POST:
            form = PersonSearchForm(request.POST)
            if form.is_valid():
                try:
                    employees = employees.filter(id=int(form.cleaned_data['name']))
                    data = {'employees': employees, 'form': form}
                except:
                    employees = employees.filter(name__icontains=form.cleaned_data['name'])
                    data = {'employees': employees, 'form': form}
                finally:
                    return render(request, 'admin/records.html', data)
        data = {'employees': employees, 'form': PersonSearchForm()}
        return render(request, 'admin/records.html', data)
    return HttpResponseNotFound()


def approve_payment(request, id):
    if request.user.is_superuser and request.user.is_authenticated:
        employee = Employee.objects.get(id=id)
        employee.receivedAmount = 0
        employee.receivedBottle = 0
        employee.save()
        for order in Order.objects.filter(delivered_by=employee, frequency='2', delivered=True):
            order.delivered = False
            order.save()
        return redirect('records')
    return HttpResponseNotFound()
