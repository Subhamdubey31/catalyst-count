# forms.py
from django import forms
from django.contrib.auth.models import User

class UserCreationForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='Active', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'status']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
