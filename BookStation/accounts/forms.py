from django.contrib.auth.forms import UserCreationForm
from .models import Users

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'phone','firstname','lastname'   )