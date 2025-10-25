from django.shortcuts import render, redirect
from .models import Quiz, Student, Question, Attempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='quiz:login')
def student_dashboard_view(request):
    user = request.user

    try:
        student_obj = user.student
        if student_obj is None:
            messages.error(request, 'Student record not found.')
            return redirect('quiz:login')
        # get the class the current user is enrolled in
        class_enrolled = student_obj.class_enrolled
        if not class_enrolled:
            return redirect('quiz:login')

        from django.utils import timezone
        current_time = timezone.now()
        
        # get all quizzes for the current user class with due status
        all_quizzes = student_obj.get_quizzes()

        active_quizzes = [quiz for quiz in all_quizzes if quiz.start_date <= current_time <= quiz.due_date]

        upcoming_quizzes = [quiz for quiz in all_quizzes if quiz.start_date > current_time]

        expired_quizzes = [quiz for quiz in all_quizzes if quiz.due_date < current_time]

        # overall metrics
        avg_score = student_obj.average_score()
        quizzes_taken = student_obj.total_quizzes_taken()
        subjects_count = student_obj.subjects_covered_count()

        context = {
            'user': user,
            'active_quizzes': active_quizzes,
            'upcoming_quizzes': upcoming_quizzes,
            'current_time': current_time,
            'average_score': f"{avg_score}%" if avg_score is not None else '0',
            'quizzes_taken': quizzes_taken,
            'subjects_covered': subjects_count,
        }
        return render(request, 'students/student-dashboard.html', context)

    except Student.DoesNotExist:
        print("Student does not exist.")
        return redirect('quiz:login')

@login_required(login_url='quiz:login')
def all_quizzes_view(request):
    user = request.user

    try:
        student_obj = user.student

        from django.utils import timezone
        current_time = timezone.now()

        # get all quizzes for the current user class for the subject the current user is enrolled

        class_quizzes = student_obj.get_quizzes()
         # if no quizzes found, return with message
        if not class_quizzes:
            return render(request, 'students/view-all-quizzes.html', {'message': 'You do not have quiz history.'})

        context = {
            'user': user,
            'all_quizzes': class_quizzes,
            'current_time': current_time,
        }

    except Student.DoesNotExist:
        print("Student record not found.")
        messages.error(request, 'Student record not found.')
        return redirect('student-dashboard')

    return render(request, 'students/view-all-quizzes.html', context)

@login_required(login_url='quiz:login')
def quiz_history_view(request, student_id=None):
    # Show the quiz history for the logged-in student

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
            'average_score': f"{avg_score}%" if avg_score is not None else '0',
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

@login_required(login_url='quiz:login')
def quiz_details_view(request, quiz_id):

    try:
        quiz = Quiz.objects.filter(pk=quiz_id).first()
        if quiz is None:
            messages.error(request, 'Quiz not found.')
            return redirect('student-dashboard')
        total = Question.objects.filter(quiz=quiz.id).count()

        from django.utils import timezone
        current_time = timezone.now()

        context = {
            'quiz': quiz,
            'total': total,
            'current_time': current_time
        }
        return render(request, 'students/quiz-details.html', context=context)

    except Exception as e:
        print('Error in quiz_details_view:', e)
        messages.error(request, 'Unable to load quiz details.')
        return redirect('student-dashboard')

@login_required(login_url='quiz:login')
def attempt_quiz_view(request, quiz_id):

    quiz = Quiz.objects.filter(pk=quiz_id).first()

    if quiz is None:
        messages.error(request, 'Quiz not found.')
        return redirect('quiz:student-dashboard')

    # get question and choices for the quiz
    questions = quiz.get_questions_with_choices()

    questions_count = len(questions)
 
    context = {
        'quiz': quiz,
        'questions': questions,
        'questions_count': questions_count,
    }

    return render(request, 'students/quiz-page.html', context=context)

@login_required(login_url='quiz:login')
def quiz_results_view(request, quiz_id):

    return render(request, 'students/quiz-results.html')

@login_required(login_url='quiz:login')
def student_profile_view(request):

    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'students/student-profile.html', context)