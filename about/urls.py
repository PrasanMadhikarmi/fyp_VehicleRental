from django.urls.conf import include
from django.urls import path

from . import views

app_name='about'

urlpatterns = [
    path("", views.about_index, name="about_index")
]