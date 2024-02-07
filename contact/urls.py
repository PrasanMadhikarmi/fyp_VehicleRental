from django.urls.conf import include
from django.urls import path

from . import views

app_name='contact'

urlpatterns = [
    path("", views.contact_index, name="contact_index"),
    path("success", views.success, name="success")
]
