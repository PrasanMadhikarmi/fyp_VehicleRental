# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings

from accounts.models import VehicleImage, VehicleRegistration

from .forms import CreateUserForm, VehicleImageFormSet, VehicleRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect ('home:index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:success')
            else:
                messages.error(request, "Error")

    context ={
        'form':form
    }
    return render(request, 'accounts/register.htm',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect ('home:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username, password=password)

            if username and password != '':
                if user is not None:
                    login(request,user)
                    return redirect('home:index')
                else:
                    messages.info(request, "*Username or password is incorrect")
            else:
                messages.info(request, "*Enter username and password")

        context={

        }
    return render(request, "accounts/login.htm")

def success(request): 
    return render(request, "accounts/success.htm")

def successRegistration(request): 
    return render(request, "accounts/success_registration.htm")

def logoutUser(request):
    logout(request)
    return redirect('home:index')



def vehicle_registration(request):
    if request.method == 'POST':
        form = VehicleRegistrationForm(request.POST, request.FILES)
        formset = VehicleImageFormSet(request.POST, request.FILES)


        vehicle_registration = form.save(commit=False)
        vehicle_registration.user = request.user  # Assign the current user
        vehicle_registration.save()

        for form in formset:
            if form.cleaned_data:
                image = form.cleaned_data['image']
                vehicle_image = VehicleImage(vehicle=vehicle_registration, image=image)
                vehicle_image.save()
        
        # Redirect to a success page or do something else upon successful registration.
        return redirect('accounts:successreg')
   

    else:
        form = VehicleRegistrationForm()
        formset = VehicleImageFormSet()

    return render(request, 'accounts/vehicleRegistration.html', {'form': form, 'formset': formset})