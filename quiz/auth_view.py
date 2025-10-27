from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, ChangePasswordForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# define the custom user model
User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if not username or not password:
                messages.error(request, 'Wrong username or password.')
                return HttpResponseRedirect(reverse('quiz:login'))
            
            # Check if the user exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Wrong username or password.')
                return HttpResponseRedirect(reverse('quiz:login'))

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, 'Wrong username or password.')
                return HttpResponseRedirect(reverse('quiz:login'))

            login(request, user)
            
            if user.role == 'student':
                return HttpResponseRedirect(reverse('quiz:student-dashboard'))
            
            elif user.role == 'teacher':
                # Redirect the teacher to the teacher-dashboard
                return HttpResponseRedirect(reverse('quiz:student-dashboard'))
    else:
        form = LoginForm()
    return render(request, 'students/login.html', {'form': form, 'title': 'Login'})

@login_required(login_url='quiz:login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('quiz:index'))

@login_required(login_url='quiz:login')
def change_password(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            # validate password
            if not str(confirm_password).isalnum() or not str(new_password).isalnum():
                messages.error(request, 'Password must container letters, numbers and capital letters.')
                return redirect('quiz:change-password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('quiz:change-password')
            
            if not confirm_password or not new_password:
                messages.error(request, 'Password fields can not be empty.')
                return redirect('quiz:change-password')
            
            if len(new_password) < 8:
                messages.error(request, 'Password is too short. Atleast 8 characters.')
                return redirect('quiz:change-password')

            instance = User.objects.get(pk=user.id)

            if instance:
                instance.set_password(new_password)
                instance.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('quiz:student-profile')
            else:
                messages.error("User not found.")
    else:
        form = ChangePasswordForm()
    return render(request, 'students/change-password.html', {'form': form, 'title': 'Change Password'})
