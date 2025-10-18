from django import forms
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, strip=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=30, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")