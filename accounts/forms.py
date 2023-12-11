from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from accounts.models import VehicleRegistration
from django.forms import inlineformset_factory


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name','username', 'email', 'password1', 'password2']



class VehicleRegistrationForm(forms.ModelForm):
    features = forms.MultipleChoiceField(
        choices=VehicleRegistration.vehicle_feature, 
        widget=forms.CheckboxSelectMultiple,
        required=False  # Set to False if not mandatory
    )

    class Meta:
        model = VehicleRegistration
        fields = ['brand', 'model', 'year', 'color', 'transmission', 'bootCapacity', 'carFuel', 'features', 'location', 'price', 'capacity', 'category', 'cc', 'subcategory', 'description', 'image1', 'image2', 'image3', 'image4', 'image5', 'bluebookimg', 'citizenimg', 'isVerified', 'available']


