# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf import settings

from .models import UserAddress

from .forms import CreateUserForm
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

def logoutUser(request):
    logout(request)
    return redirect('home:index')