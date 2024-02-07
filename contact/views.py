from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from .models import Contact
from django.contrib import messages


# Create your views here.

def contact_index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and messages != '':
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            current_user = request.user
            print(f"The user that send this message is {current_user}")
            return redirect('contact:success')

    return render(request,'contact/contact.htm')

def success(request): 
    return render(request, "contact/success.htm")


