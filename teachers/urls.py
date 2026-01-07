from django.urls import path
from . import views 
from django.conf.urls import handler404, handler500

app_name = 'teachers'

urlpatterns=[
      path('dashboard/', views.teacher_dashboard_view, name='dashboard'),
      path('quizzes/', views.all_quizzes_view, name='all-quizzes'),
      path('students/', views.students_view, name='students'),
      path('student/<int:student_id>/edit/', views.edit_student, name='edit-student'),
      path('student/<int:student_id>/delete/', views.delete_student, name='delete-student'),
      path('reports/', views.reports_view, name='reports'),
      path('subjects/', views.subjects_view, name='subjects'),
      path('quiz/<int:quiz_id>', views.view_quiz_details, name='quiz-details'),
      path('profile', views.teacher_profile_view, name='profile'),
      path('quiz/create/', views.create_quiz_view, name='create-quiz'),
      path('quiz/delete/<int:quiz_id>', views.delete_quiz_view, name='delete-quiz'),
]

handler404 = 'teachers.views.custom_page_not_found_view'
handler500 = 'teachers.views.custom_server_error_view'