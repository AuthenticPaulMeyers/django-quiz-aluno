from django.urls import path
from . import views 

app_name = 'teachers'

urlpatterns=[
      path('dashboard/', views.teacher_dashboard_view, name='dashboard'),
      path('quizzes/', views.all_quizzes_view, name='all-quizzes'),
]