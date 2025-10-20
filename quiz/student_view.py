from django.shortcuts import render, redirect
from .models import Quiz, Student, Question
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def student_dashboard_view(request):
    if request.user.is_authenticated:
        user = request.user

        try:
            student_obj = user.student
            # get the class the current user is enrolled in
            class_enrolled = student_obj.class_enrolled

            # get the quizzes all quizzes for the current user class
            class_quizzes = Quiz.objects.filter(quizclass=class_enrolled.id).all()
            
            if not class_quizzes:
                return render(request, 'students/student-dashboard.html', {'message': 'You do not have active quizzes.'})
            
            context = {
                'user': user,
                'all_quizzes': class_quizzes
            }

        except Student.DoesNotExist:
            print("Student does not exist.")

        return render(request, 'students/student-dashboard.html', context)

def all_quizzes_view(request):
    if request.user.is_authenticated:
        user = request.user

        try:
            student_obj = user.student
            # get the class the current user is enrolled in
            class_enrolled = student_obj.class_enrolled

            # get the quizzes all quizzes for the current user class
            class_quizzes = Quiz.objects.filter(quizclass=class_enrolled.id).all()
            
            if not class_quizzes:
                return render(request, 'students/view-all-quizzes.html', {'message': 'You do not have active quizzes.'})
            
            context = {
                'user': user,
                'all_quizzes': class_quizzes
            }

        except Student.DoesNotExist:
            print("Student does not exist.")

    return render(request, 'students/view-all-quizzes.html', context)

def quiz_history_view(request, student_id=None):
    # Show the quiz history for the logged-in student
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    try:
        # prefer the logged-in user's student object
        student_obj = getattr(user, 'student', None)
        if student_obj is None and student_id:
            # fallback: try to get by id
            from .models import Student
            student_obj = Student.objects.filter(pk=student_id).first()

        if student_obj is None:
            messages.error(request, 'Student record not found.')
            return redirect('student-dashboard')

        # overall metrics
        avg_score = student_obj.average_score()
        quizzes_taken = student_obj.total_quizzes_taken()
        subjects_count = student_obj.subjects_covered_count()
        subject_perf = student_obj.subject_performance()

        context = {
            'user': user,
            'average_score': f"{avg_score}%" if avg_score is not None else 'N/A',
            'quizzes_taken': quizzes_taken,
            'subjects_covered': subjects_count,
            'subject_performance': subject_perf,
        }

        return render(request, 'students/quiz-history.html', context)

    except Exception as e:
        # for debugging purposes
        print('Error in quiz_history_view:', e)
        messages.error(request, 'Unable to load quiz history.')
        return redirect('student-dashboard')

def quiz_details_view(request, quiz_id):
    quiz = Quiz.objects.filter(pk=quiz_id).first()
    total = Question.objects.filter(quiz=quiz.id).count()

    context = {
        'quiz': quiz,
        'total': total
    }
    return render(request, 'students/quiz-details.html', context=context)

def attempt_quiz_view(request, quiz_id):
    return render(request, 'students/quiz-page.html')

def quiz_results_view(request):
    return render(request, 'students/quiz-results.html')

def student_profile_view(request, student_id):
    return render(request, 'students/student-profile.html')