from django.shortcuts import render, redirect
from quiz.models import Quiz, Student, Question, Attempt, MultipleChoice, AttemptAnswer
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Dashboard
@login_required(login_url='quiz:login')
def teacher_dashboard_view(request):
      user = request.user

      context={
            'user': user,
            'title': 'Dashboard',
      }
      return render(request, 'teachers/teacher-dashboard.html', context)

# All quizzes
@login_required(login_url='quiz:login')
def all_quizzes_view(request):
      user = request.user

      context={
            'user': user,
            'title': 'All Quizzes',
      }
      return render(request, 'teachers/all_quizzes.html', context)


