from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm
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
    return render(request, 'login.html', {'form': form})

# @login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('quiz:index'))