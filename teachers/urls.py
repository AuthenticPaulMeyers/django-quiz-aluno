from django.urls import path
from . import views 

app_name = 'teachers'

urlpatterns=[
      path('dashboard/', views.teacher_dashboard_view, name='dashboard'),
      path('quizzes/', views.all_quizzes_view, name='all-quizzes'),
      path('classes/', views.classes_view, name='classes'),
      path('reports/', views.reports_view, name='reports'),
      path('subjects/', views.subjects_view, name='subjects'),
]