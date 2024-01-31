# Create your views here.
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from accounts.models import UserAddress, UserVerificationStatus, VehicleRegistration
from services.models import CustomerPayment

from .forms import CreateUserForm, VehicleRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('home:index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                # Log in the user
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(
                    request, username=username, password=password)
                login(request, user)

                # Create UserVerificationStatus for the newly registered user
                UserVerificationStatus.objects.create(user=user)

                return redirect('home:index')
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
        print('submission')
        form = VehicleRegistrationForm(request.POST, request.FILES)

        # Save the vehicle registration data
        vehicle_registration = form.save(commit=False)
        vehicle_registration.user = request.user
        vehicle_registration.save()
        print('submitted')

        # Redirect to a success page or do something else upon successful registration.
        return redirect('accounts:successreg')

    else:
        form = VehicleRegistrationForm()

    return render(request, 'accounts/vehicleRegistration.html', {'form': form})


def userProfile(request):
    current_user = request.user
    user_verification_status = UserVerificationStatus.objects.get(
        user=request.user)

    data = User.objects.get(id=current_user.id)
    if UserAddress.objects.filter(user_info_id=current_user.id).exists():
        data2 = UserAddress.objects.get(user_info_id=current_user.id)
    else:
        data2 = "Enter Detail"

    if request.user.is_authenticated:
        if request.method == 'POST':
            user_info_id = request.user.id
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
         # Calculate total unpaid amount to vendor
        total_unpaid_to_vendor = CustomerPayment.objects.filter(
            booking_id__vehicle_id__user=current_user, vendor_paid_status=False
        ).aggregate(Sum('vendor_payment'))['vendor_payment__sum'] or 0

        # Calculate total amount paid to vendor
        total_paid_to_vendor = CustomerPayment.objects.filter(
            booking_id__vehicle_id__user=current_user, vendor_paid_status=True
        ).aggregate(Sum('vendor_payment'))['vendor_payment__sum'] or 0

        context = {
            'user': data,
            'address': data2,
            'total_unpaid_to_vendor': total_unpaid_to_vendor,
            'total_paid_to_vendor': total_paid_to_vendor,
            'user_verification_status': user_verification_status
        }

        return render(request, "accounts/profile.html", context)


@login_required
def verification_view(request):
    user = request.user
    verification_model = UserVerificationStatus.objects.get(user=user)
    verification_model.reverify = False
    verification_model.save()

    if request.method == 'POST':
        handle_uploaded_file(request.FILES.get(
            'user_photo'), verification_model, 'user_photo')
        handle_uploaded_file(request.FILES.get(
            'citizen_ship_image'), verification_model, 'citizen_ship_image')
        send_mail(f'Verification Request from {user.username}', f'{user.username} has requested for their profile verification.\n Please redirect to this URL to verify the profile: http://127.0.0.1:8000/admin/accounts/userverificationstatus/{verification_model.id}/change/', 'eliterental.helpline@gmail.com',
                  ['rentalsu.elite@gmail.com'], fail_silently=False)

    return redirect('accounts:profile')


def handle_uploaded_file(file, model_instance, file_field):
    if file:
        file_path = default_storage.save(
            f'accounts/{file_field}/{file.name}', ContentFile(file.read()))
        setattr(model_instance, file_field, file_path)
        model_instance.save()


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
    print(vehicle_id)
    vehicle = VehicleRegistration.objects.get(id=vehicle_id)
    request_user = vehicle.user

    if request.method == 'POST':
        form = VehicleRegistrationForm(
            request.POST, request.FILES, instance=vehicle)

        # Check if there are changes in fields other than 'available'
        if form.has_changed() and ('available' not in form.changed_data or len(form.changed_data) > 1):
            form.save()
            # vehicle.isVerified = False
            # vehicle.available = False
            # vehicle.save()

            # Send email only if there are changes other than 'available'
            print(form.cleaned_data)
            send_mail('Verification regarding Vehicle Update', f'{request_user.username} has requested for vehicle verification for their edit.\n Please redirect to this URL to verify the vehicle: http://127.0.0.1:8000/admin/accounts/vehicleregistration/{vehicle_id}/change/', 'eliterental.helpline@gmail.com',
                      ['rentalsu.elite@gmail.com'], fail_silently=False)

        else:
            # No changes or only 'available' field changed, no need to send email
            form.save()

        return redirect('accounts:myvehicles')
    else:
        form = VehicleRegistrationForm(instance=vehicle)

    return redirect('accounts:myvehicles')
