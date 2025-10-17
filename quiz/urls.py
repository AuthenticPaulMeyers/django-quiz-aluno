from django.urls import path
from . import views, auth, student_view, teacher_view

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout')
]