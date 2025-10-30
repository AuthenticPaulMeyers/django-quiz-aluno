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
      return render(request, 'teachers/all-quizzes.html', context)

#view classes
@login_required(login_url='quiz:login')
def classes_view(request):
      user = request.user

      context={
            'user': user,
            'title': 'Classes'
      }
      return render(request, 'teachers/classes.html', context)

#view reports
@login_required(login_url='quiz:login')
def reports_view(request):
      user = request.user

      context={
            'user': user,
            'title': 'Reports'
      }
      return render(request, 'teachers/reports.html', context)

#view reports
@login_required(login_url='quiz:login')
def subjects_view(request):
      user = request.user

      context={
            'user': user,
            'title': 'Subjects'
      }
      return render(request, 'teachers/subjects.html', context)

