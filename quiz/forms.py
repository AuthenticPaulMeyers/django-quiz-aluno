from django import forms
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser

# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, strip=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=30, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Change password form
class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=40, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    confirm_password = forms.CharField(max_length=40, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

# Admin create user form
class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")

