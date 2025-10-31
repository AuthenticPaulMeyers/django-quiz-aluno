from django.urls import path
from . import views 

app_name = 'teachers'

urlpatterns=[
      path('dashboard/', views.teacher_dashboard_view, name='dashboard'),
      path('quizzes/', views.all_quizzes_view, name='all-quizzes'),
      path('students/', views.students_view, name='students'),
      path('reports/', views.reports_view, name='reports'),
      path('subjects/', views.subjects_view, name='subjects'),
      path('quiz/<int:quiz_id>', views.view_quiz_details, name='quiz-details'),
      path('profile', views.teacher_profile_view, name='profile'),
]