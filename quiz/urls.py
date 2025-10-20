from django.urls import path
from . import auth_view, views, student_view, teacher_view

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    # Auth view
    path('login/', auth_view.login_view, name='login'),
    path('logout/', auth_view.logout_view, name='logout'),
    # Student view
    path('student/dashboard/', student_view.student_dashboard_view, name='student-dashboard'),
    path('student/all-quizzes/', student_view.all_quizzes_view, name='all-quizzes'),
    path('student/quiz-history/<int:student_id>', student_view.quiz_history_view, name='quiz-history'),
    path('student/profile', student_view.student_profile_view, name='student-profile'),
    path('student/quiz-details/<int:quiz_id>', student_view.quiz_details_view, name='quiz-details'),
    path('student/attempt-quiz/<int:quiz_id>', student_view.attempt_quiz_view, name='attempt-quiz'),
    path('student/quiz-results/<int:quiz_id>', student_view.quiz_results_view, name='quiz-results'),
    # Teacher view
]