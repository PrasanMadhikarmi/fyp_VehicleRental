from django import forms
from .models import bookInstantly


class BookingForm(forms.ModelForm):
    class Meta:
        model = bookInstantly
        fields = ['name', 'email', 'number', 'pickDate', 'pickTime',
                  'dropDate', 'dropTime']


