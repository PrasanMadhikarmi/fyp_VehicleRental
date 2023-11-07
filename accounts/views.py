# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings

from accounts.models import UserAddress, VehicleRegistration

from .forms import CreateUserForm, VehicleRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('home:index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:success')
            else:
                messages.error(request, "Error")

    context = {
        'form': form
    }
    return render(request, 'accounts/register.htm', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if username and password != '':
                if user is not None:
                    login(request, user)
                    return redirect('home:index')
                else:
                    messages.info(
                        request, "*Username or password is incorrect")
            else:
                messages.info(request, "*Enter username and password")

        context = {

        }
    return render(request, "accounts/login.htm")


def success(request):
    return render(request, "accounts/success.htm")


def successRegistration(request):
    return render(request, "accounts/success_registration.htm")


def logoutUser(request):
    logout(request)
    return redirect('home:index')


@login_required
def vehicle_registration(request):
    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST, request.FILES)

            
        # Save the vehicle registration data
        vehicle_registration = form.save(commit=False)
        vehicle_registration.user = request.user
        vehicle_registration.save()

        # Redirect to a success page or do something else upon successful registration.
        return redirect('accounts:successreg')

    else:
        form = VehicleRegistrationForm()

    return render(request, 'accounts/vehicleRegistration.html', {'form': form})


def userProfile(request):
    current_user = request.user

    data = User.objects.get(id=current_user.id)
    if UserAddress.objects.filter(user_info_id=current_user.id).exists():
        data2 = UserAddress.objects.get(user_info_id=current_user.id)
    else:
        data2 = "Enter Detail"

    if request.user.is_authenticated:
        if request.method == 'POST':
            user_info_id = request.POST.get('UserId')
            address_name = request.POST.get('address')
            street = request.POST.get('street')
            postalcode = request.POST.get('postalcode')
            city = request.POST.get('city')
            country = request.POST.get('country')

            if address_name and street and postalcode and city and country != '':
                address_data = UserAddress(user_info_id=user_info_id, address=address_name,
                                           street=street, postalcode=postalcode, city=city, country=country)
                address_data.save()
                current_user = request.user
                print(f"address saved")
                data2 = UserAddress.objects.get(user_info_id=current_user.id)
            else:
                print("empty")
        context = {
            'user': data,
            'address': data2
        }

        return render(request, "accounts/profile.html", context)


def myVehicles(request):
    # Get all vehicles associated with the logged-in user
    user_vehicles = VehicleRegistration.objects.filter(user=request.user)

    context = {
        'user_vehicles': user_vehicles
    }

    return render(request, "accounts/my_vehicles.html", context)


def delete_vehicle(request, vehicle_id):
    vehicle = VehicleRegistration.objects.get(id=vehicle_id)
    vehicle.delete()
    return redirect('accounts:myvehicles')  # Redirect to 'myvehicles' page


def edit_vehicle(request, vehicle_id):
    vehicle = VehicleRegistration.objects.get(id=vehicle_id)

    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST, instance=vehicle)
        form.save()
        return redirect('accounts:myvehicles')
    else:
        form = VehicleRegistrationForm(instance=vehicle)

    return redirect('accounts:myvehicles')
