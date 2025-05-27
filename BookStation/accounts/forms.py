from django.contrib.auth.forms import UserCreationForm
from .models import Users
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'phone','first_name','last_name' )

class EditProfile(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'phone','first_name','last_name' )