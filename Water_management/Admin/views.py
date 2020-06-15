from django.shortcuts import render
from database.models import Person, Customer, Order, City, Area, Vehicle, Schedule
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .forms import CustomerEditForm, ScheduleCreateForm, EmployeeCreateForm, VehicleCreateForm, AreaCreateForm, \
    CityCreateForm

def home(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'orders': Order.objects.filter(delivered=False)
        }
        if request.user.is_superuser:
            return render(request, 'home.html', context)
    return render(request, 'home.html')

def details_view(request, username=None, *args, **kwargs):
    if request.POST and request.user.is_superuser:
        selection = request.POST.get('selected')
        NoOfBottles = request.POST.get('NoOfBottles')
        MonthlyBill = request.POST.get('MonthlyBill')
        AmountDue = request.POST.get('AmountDue')
        user = Customer.objects.filter(username=username)
        if selection == "1":
            user.update(is_approved=True, is_available=True)
            return redirect('/admin/home/')
        if selection == "2":
            user.update(is_approved=False)
            return redirect('/admin/home/')
        if selection == "3":
            user.update(is_available=False, is_approved=False)
            return redirect('/admin/home/')
        user.update(NoOfBottles=NoOfBottles, MonthlyBill=MonthlyBill, AmountDue=AmountDue)
        return redirect('/admin/home/')

        # customer ki info edit kro
        return redirect('/admin/home/')
    elif request.user.is_authenticated and (request.user.is_superuser or request.user.username == username):
        instance = get_object_or_404(Person, username=username)
        if instance.is_customer:
            instance = get_object_or_404(Customer, username=username)
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
        data = {"allEmployee": employee, 'requesting': request.user}
        return render(request, "admin/allEmployee.html", data)  # Add this Template later
    return HttpResponseNotFound()


def all_orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.all()
        data = {"orders": orders, 'requesting': request.user}
        return render(request, "admin/allOrder.html", data)  # Add this Template later
    return HttpResponseNotFound()


def add_city(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            form = CityCreateForm(request.POST)
            if form.is_valid():
                form.save()
                data = {"message": "City Added Successfully!", "form": CityCreateForm()}
            else:
                data = {"message": "Invalid Data Please Retry!", "form": form}
            return render(request, 'admin/newCity.html', data)  # Add this template later
        return render(request, 'admin/newCity.html', {'form': CityCreateForm()})
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
        if request.POST:
            form = VehicleCreateForm(request.POST)
            if form.is_valid():
                form.save()
                data = {"message": "Vehicle Added Successfully!", "form": VehicleCreateForm()}
            else:
                data = {"message": "Invalid Data Please Retry!", "form": form}
            return render(request, 'admin/newVehicle.html', data)  # Add this template later
        return render(request, 'admin/newVehicle.html', {'form': VehicleCreateForm()})
    return HttpResponseNotFound()


def all_vehicle(request):
    if request.user.is_authenticated and request.user.is_superuser:
        vehicles = Vehicle.objects.all()
        data = {"vehicles": vehicles, 'requesting': request.user}
        return render(request, "admin/allVehicle.html", data)  # Add this Template later
    return HttpResponseNotFound()


def update_schedule(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.POST:
            filled_form = ScheduleCreateForm(request.POST)
            if filled_form.is_valid():
                try:
                    schedule = Schedule.objects.get(day=filled_form.cleaned_data['day'])
                    updateForm = ScheduleCreateForm(request.POST, instance=schedule)
                    if updateForm.is_valid():
                        updateForm.save()
                        data = {'message': 'Schedule Updates Successfully!', 'form': ScheduleCreateForm()}
                    else:
                        data = {'message': 'Schedule Updates Unsuccessful Please Retry!', 'form': ScheduleCreateForm()}
                except:
                    filled_form.save()
                    data = {'message': 'Schedule Updates Successfully!', 'form': ScheduleCreateForm()}
                finally:
                    return render(request, 'admin/updateScedule.html', data)  # create this template later
            data = {'message': 'Schedule Updates Unsuccessful Please Retry!', 'form': ScheduleCreateForm()}
            return render(request, 'admin/updateScedule.html', data)
        data = {'form': ScheduleCreateForm()}
        return render(request, 'admin/updateScedule.html', data)
    return HttpResponseNotFound()


def show_schedule(request):
    if request.user.is_authenticated and request.user.is_superuser:
        schedule = Schedule.objects.all()
        data = {'schedule': schedule, "requesting": request.user}
        return render(request, 'admin/schedule.html', data)  # add this template later
