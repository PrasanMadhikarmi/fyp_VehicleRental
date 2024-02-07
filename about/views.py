from django.shortcuts import render
from django.http import HttpResponse, response

# Create your views here.

def about_index(request):
    return render(request,'about/AboutUs.html')
