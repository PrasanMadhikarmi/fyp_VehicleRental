from django.urls import path


from . import views

app_name = 'services'

urlpatterns = [
    path("vehicle_display", views.vehicleDisplay, name="vehicle_display"),
    path('detail/<int:car_id>', views.detail, name="detail"),
]
