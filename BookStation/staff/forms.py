from django.contrib.auth.forms import UserCreationForm
from accounts.models import Users
from django import forms

#
# class CustomUserCreationForm(UserCreationForm):
#     phone = forms.CharField(max_length=12, required=True)
#     class Meta:
#         model = Users
#         fields = ('username', 'email', 'phone','first_name','last_name' )
#
#     def clean_phone(self):
#        phone = self.cleaned_data.get('phone')
#        if not phone:
#            raise forms.ValidationError("Số điện thoại không được để trống")
#        return phone
#
# class CustomUserChangeForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ('email', 'phone', 'first_name', 'last_name')
#
#     def clean_phone(self):
#         phone = self.cleaned_data.get('phone')
#         if not phone:
#             raise forms.ValidationError("Số điện thoại không được để trống")
#         return phone