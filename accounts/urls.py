from django.urls.conf import include
from django.urls import path

from . import views

app_name='accounts'

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.loginPage, name="loginPage"),
    path("logout", views.logoutUser, name="logout"),
    path("success", views.success, name="success"),
    path("success_registration", views.successRegistration, name="successreg"),
    path('vehicle_registration/', views.vehicle_registration, name='vehicle_registration'),
    path("profile", views.userProfile,name="profile")
]