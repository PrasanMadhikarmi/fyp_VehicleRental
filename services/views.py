from django.shortcuts import render

from accounts.models import VehicleRegistration
from datetime import datetime

from services.models import bookInstantly

# Create your views here.

def vehicleDisplay(request):
    context={}
    if request.method == 'POST':
        location = request.POST.get('location')
        from_date = request.POST.get('from')
        until_date = request.POST.get('until')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')

        user_vehicles = VehicleRegistration.objects.filter(isVerified=True, available=True)

        if user_vehicles.exists():
            # Filter vehicles based on form data
            user_vehicles = user_vehicles.filter(
                location__icontains=location,
                category=category,
                subcategory=subcategory
            )

            print(user_vehicles)

            context = {
                'user_vehicles': user_vehicles,
                'category':category
            }
        else:
            context = {
                'no_results': True
            }

        return render(request, "services/display.html", context)

    return render(request, "services/display.html",context)

