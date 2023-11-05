from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from accounts.models import VehicleImage, VehicleRegistration
from django.forms import inlineformset_factory


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name','username', 'email', 'password1', 'password2']



class VehicleRegistrationForm(forms.ModelForm):
    class Meta:
        model = VehicleRegistration
        fields = ['brand', 'model', 'location', 'price', 'capacity', 'category', 'description']

VehicleImageFormSet = inlineformset_factory(VehicleRegistration, VehicleImage, fields=('image',), extra=7)

