from django.shortcuts import render, redirect
from quiz.models import Quiz, Student, Question, Attempt, MultipleChoice, AttemptAnswer, Teacher, TeacherSubjectClass, SubjectTeacher
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Dashboard
@login_required(login_url='quiz:login')
def teacher_dashboard_view(request):
      user = request.user

      # First check if user has teacher role
      if user.role != 'teacher':
            messages.error(request, 'Access denied. You are not registered as a teacher.')
            return redirect('quiz:login')

      try:
            teacher_obj = user.teacher
            
            if teacher_obj is None:
                  messages.error(request, 'Teacher records not found.')
                  return redirect('quiz:login')
            
            # get number of classes taught by this teacher
            classes_count = teacher_obj.classes_count()

            # get number of subjects taught by this teacher
            subjects_count = teacher_obj.subjects_count()

            # get number of quizzes created by this teacher
            quizzes_count = teacher_obj.quizzes_count()

            #get all the quizzes for this current teacher
            quizzes = teacher_obj.get_quizzes()

            from django.utils import timezone
            current_time = timezone.now()

            # get active quizzes
            active_quizzes = [quiz for quiz in quizzes if quiz.start_date <= current_time <= quiz.due_date]
            
            context={
                  'user': user,
                  'title': 'Dashboard',
                  'active_quizzes': active_quizzes,
                  'classes_count': classes_count,
                  'subjects_count': subjects_count,
                  'quizzes_count': quizzes_count,
            }

            return render(request, 'teachers/teacher-dashboard.html', context)
      
      except Exception as e:
            print("User does not exist.")
            messages.error(request, 'An error occurred while accessing teacher profile.')
            return redirect('quiz:login')

# All quizzes
@login_required(login_url='quiz:login')
def all_quizzes_view(request):
      user = request.user

      # First check if user has teacher role
      if user.role != 'teacher':
            messages.error(request, 'Access denied. You are not registered as a teacher.')
            return redirect('quiz:login')
      
      try:
            teacher_obj = user.teacher
            
            if teacher_obj is None:
                  messages.error(request, 'Teacher records not found.')
                  return redirect('quiz:login')

            # get number of quizzes created by this teacher
            quizzes_count = teacher_obj.quizzes_count()

            #get all the quizzes for this current teacher
            quizzes = teacher_obj.get_quizzes()

            from django.utils import timezone
            current_time = timezone.now()

            context={
                  'user': user,
                  'title': 'Dashboard',
                  'quizzes': quizzes,
                  'current_time': current_time,
                  'quizzes_count': quizzes_count,
            }

            return render(request, 'teachers/all-quizzes.html', context)

      except Exception as e:
            print("User does not exist.")
            messages.error(request, 'An error occurred while accessing teacher profile.')
            return redirect('quiz:login')

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

# Quiz details
@login_required(login_url='qioz:login')
def view_quiz_details(request, quiz_id):
      user = request.user

      try:
            quiz = Quiz.objects.filter(pk=quiz_id).first()

            if quiz is None:
                  messages.error(request, 'Quiz not found.')
                  return redirect('teachers:dashboard')
            
            total_questions = Question.objects.filter(quiz=quiz.id).count()

            context={
                  'user': user,
                  'title': 'Quiz Details',
                  'quiz': quiz,
                  'total_questions': total_questions,
            }

            return render(request, 'teachers/quiz-details.html', context)
      
      except Exception as e:
            messages.error(request, 'Quiz not found.')
            print(e)
            return redirect('teachers:dashboard')
      

@login_required(login_url='quiz:login')
def teacher_profile_view(request):

    user = request.user
    context = {
        'user': user,
        'title': 'Teacher Profile',
    }
    return render(request, 'teachers/teacher-profile.html', context)