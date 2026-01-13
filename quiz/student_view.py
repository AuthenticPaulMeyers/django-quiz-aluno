import logging
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)
from .models import Quiz, Student, Question, Attempt, MultipleChoice, AttemptAnswer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import close_old_connections
from .utils import check_student_grade

@login_required(login_url='quiz:login')
def student_dashboard_view(request):
    # Close old database connections to prevent connection pool overflow
    close_old_connections()

    user = request.user
    # First check if user has student role
    if user.role != 'student':
        messages.error(request, 'Access denied. You are not registered as a student.')
        return redirect('quiz:login')
    
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
        current_time = timezone.localtime(timezone.now())
        
        # get all quizzes for the current user class with due status
        all_quizzes = student_obj.get_quizzes().select_related(
            'teacher_subject_class__subject_teacher__subject',
            'teacher_subject_class__subject_teacher__teacher__user'
        )

        # exclude quizzes already completed by this student (consider them 'expired' for this student)

        completed_quiz_ids = set(
            Attempt.objects.filter(student=student_obj, is_completed=True).values_list('quiz_id', flat=True)
        )

        active_quizzes = [
            quiz for quiz in all_quizzes 
            if quiz.start_date <= current_time <= quiz.due_date and quiz.id not in completed_quiz_ids
        ]

        upcoming_quizzes = [
            quiz for quiz in all_quizzes 
            if quiz.start_date > current_time and quiz.id not in completed_quiz_ids
        ]

        # expired_quizzes: those past due OR quizzes already completed by this student
        expired_quizzes = [
            quiz for quiz in all_quizzes 
            if quiz.due_date < current_time or quiz.id in completed_quiz_ids
        ]

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
            'title': 'Dashboard',
        }
        return render(request, 'students/student-dashboard.html', context)

    except Student.DoesNotExist:
        logger.error("Student does not exist.")
        return redirect('quiz:login')

@login_required(login_url='quiz:login')
def all_quizzes_view(request):
    user = request.user

    # First check if user has student role
    if user.role != 'student':
        messages.error(request, 'Access denied. You are not registered as a student.')
        return redirect('quiz:login')

    try:
        student_obj = user.student

        from django.utils import timezone
        current_time = timezone.localtime(timezone.now())

        # get all quizzes for the current user class for the subject the current user is enrolled

        class_quizzes = student_obj.get_quizzes()
         # if no quizzes found, return with message
        if class_quizzes is None:
            messages.info(request, 'You do not have exam history.')
            return redirect('quiz:all-quizzes')

        context = {
            'user': user,
            'all_quizzes': class_quizzes,
            'current_time': current_time,
            'title': 'All Exams',
        }

    except Student.DoesNotExist:
        logger.error("Student record not found.")
        messages.error(request, 'Student record not found.')
        return redirect('quiz:student-dashboard')

    return render(request, 'students/view-all-quizzes.html', context)

@login_required(login_url='quiz:login')
def quiz_history_view(request):
    # Show the quiz history for the logged-in student
    user = request.user
    try:
        # prefer the logged-in user's student object
        student_obj = getattr(user, 'student', None)
        
        if student_obj is None:
            messages.error(request, 'Student record not found.')
            return redirect('quiz:student-dashboard')

        # overall metrics
        avg_score = student_obj.average_score()
        quizzes_taken = student_obj.total_quizzes_taken()
        subjects_count = student_obj.subjects_covered_count()
        subject_perf = student_obj.subject_performance()

        # Get all attempts for this student so we can display grade per quiz taken
        attempts = Attempt.objects.filter(student=student_obj).select_related('quiz').order_by('-id')

        # get the grade
        for attempt in attempts:
            attempt.grade = check_student_grade(attempt.score)

        context = {
            'user': user,
            'average_score': f"{avg_score}%" if avg_score is not None else '0',
            'quizzes_taken': quizzes_taken,
            'subjects_covered': subjects_count,
            'subject_performance': subject_perf,
            'attempts': attempts,
            'title': 'Exam History',
        }

        return render(request, 'students/quiz-history.html', context)

    except Exception as e:
        # for debugging purposes
        logger.error(f"Error in quiz_history_view: {e}")
        messages.error(request, 'Unable to load exam history.')
        return redirect('quiz:student-dashboard')

@login_required(login_url='quiz:login')
def quiz_details_view(request, quiz_id):

    try:
        quiz = Quiz.objects.filter(pk=quiz_id).first()
        if quiz is None:
            messages.error(request, 'Exam not found.')
            return redirect('quiz:student-dashboard')
        total = Question.objects.filter(quiz=quiz.id).count()

        from django.utils import timezone
        current_time = timezone.localtime(timezone.now())

        context = {
            'quiz': quiz,
            'total': total,
            'current_time': current_time,
            'title': 'Exam Details',
        }
        return render(request, 'students/quiz-details.html', context)

    except Exception as e:
        logger.error(f"Error in quiz_details_view: {e}")
        messages.error(request, 'Unable to load exam details.')
        return redirect('quiz:student-dashboard')

@login_required(login_url='quiz:login')
def attempt_quiz_view(request, quiz_id):

    quiz = Quiz.objects.filter(pk=quiz_id).first()

    if quiz is None:
        messages.error(request, 'Exam not found.')
        return redirect('quiz:student-dashboard')

    # Prevent re-attempt if student already completed this quiz
    try:
        student_obj = request.user.student
    except Exception:
        messages.error(request, 'Student record not found.')
        return redirect('quiz:student-dashboard')

    existing = Attempt.objects.filter(student=student_obj, quiz=quiz, is_completed=True).first()
    if existing:
        messages.info(request, 'You have already completed this exam. Viewing results instead.')
        return redirect('quiz:quiz-results', quiz_id=quiz.id)

    # get question and choices for the quiz
    questions = quiz.get_questions_with_choices()

    questions_count = len(questions)
 
    context = {
        'quiz': quiz,
        'questions': questions,
        'questions_count': questions_count,
        'title': 'Attempt Exam',
    }

    return render(request, 'students/quiz-page.html', context=context)

@login_required(login_url='quiz:login')
def quiz_results_view(request, quiz_id):
    # Process POSTed answers and compute results
    quiz = Quiz.objects.filter(pk=quiz_id).first()
    if quiz is None:
        messages.error(request, 'Exam not found.')
        return redirect('quiz:student-dashboard')

    user = request.user
    try:
        student_obj = user.student
    except Exception:
        messages.error(request, 'Student record not found.')
        return redirect('quiz:student-dashboard')

    # If GET, show existing completed attempt if present; otherwise redirect to attempt page
    existing_attempt = Attempt.objects.filter(student=student_obj, quiz=quiz, is_completed=True).first()
    if request.method == 'GET':
        if existing_attempt:
            # build answers_review from stored AttemptAnswer rows
            answers = existing_attempt.get_answers().select_related('multiple_choice', 'question')
            answers_review = []
            correct_count = 0
            for ans in answers:
                your = ans.multiple_choice.choice_text if ans.multiple_choice else None
                correct = MultipleChoice.objects.filter(question=ans.question, is_correct=True).first()
                correct_text = correct.choice_text if correct else None
                if ans.is_correct:
                    correct_count += 1
                answers_review.append({
                    'question': ans.question.question_text,
                    'your_answer': your,
                    'correct_answer': correct_text,
                    'is_correct': ans.is_correct,
                })

            context = {
                'score': float(round(existing_attempt.score)),
                'grade': check_student_grade(existing_attempt.score),
                'correct_count': correct_count,
                'total': answers.count(),
                'answers_review': answers_review,
                'title': 'Exam Results',
            }
            return render(request, 'students/quiz-results.html', context)
        else:
            return redirect('quiz:attempt-quiz', quiz_id=quiz.id)

    # If a completed attempt already exists, don't create a new one — render the existing results instead
    if existing_attempt:
        answers = existing_attempt.get_answers().select_related('multiple_choice', 'question')
        answers_review = []
        correct_count = 0
        for ans in answers:
            your = ans.multiple_choice.choice_text if ans.multiple_choice else None
            correct = MultipleChoice.objects.filter(question=ans.question, is_correct=True).first()
            correct_text = correct.choice_text if correct else None
            if ans.is_correct:
                correct_count += 1
            answers_review.append({
                'question': ans.question.question_text,
                'your_answer': your,
                'correct_answer': correct_text,
                'is_correct': ans.is_correct,
            })

        context = {
            'score': existing_attempt.score,
            'grade': check_student_grade(existing_attempt.score),
            'correct_count': correct_count,
            'total': answers.count(),
            'answers_review': answers_review,
            'time_taken': None,
            'title': 'Exam Results',
        }
        return render(request, 'students/quiz-results.html', context)

    # Create an Attempt record (initial score 0, will update after grading)
    attempt = Attempt.objects.create(student=student_obj, quiz=quiz, score=0, is_completed=False)

    questions = quiz.get_questions_with_choices()
    total_questions = len(questions)
    correct_count = 0
    answers_review = []

    for qdict in questions:
        question = qdict.get('question')
        # POST keys are named question_<question.id>
        posted = request.POST.get(f'question_{question.id}')
        selected_choice = None
        is_correct = False

        if posted:
            try:
                selected_choice = MultipleChoice.objects.filter(pk=int(posted)).first()
            except Exception:
                selected_choice = None

        # Determine correct choice
        correct_choice = MultipleChoice.objects.filter(question=question, is_correct=True).first()

        if selected_choice and getattr(selected_choice, 'is_correct', False):
            is_correct = True
            correct_count += 1

        # Ensure we have a MultipleChoice reference to store (prefer student's choice, otherwise store correct choice)
        chosen_mc = selected_choice if selected_choice else (correct_choice if correct_choice else None)
        if chosen_mc is None:
            # If there is no available multiple choice for this question, skip recording the answer
            continue

        AttemptAnswer.objects.create(
            attempt=attempt,
            question=question,
            multiple_choice=chosen_mc,
            is_correct=is_correct,
        )

        answers_review.append({
            'question': question.question_text,
            'your_answer': selected_choice.choice_text if selected_choice else None,
            'correct_answer': correct_choice.choice_text if correct_choice else None,
            'is_correct': is_correct,
        })

    # compute percentage score
    score_percent = round((correct_count / total_questions) * 100) if total_questions > 0 else 0
    attempt.score = score_percent
    attempt.is_completed = True
    attempt.save()

    # compute time taken if provided
    time_taken = None
    time_remaining = request.POST.get('time_remaining')
    try:
        if time_remaining is not None and time_remaining != '':
            remaining = int(time_remaining)
            total_seconds = int(quiz.duration) * 60
            taken_seconds = max(total_seconds - remaining, 0)
            minutes = taken_seconds // 60
            secs = taken_seconds % 60
            time_taken = f"{minutes}m {secs}s"
    except Exception:
        time_taken = None

    print(score_percent)

    context = {
        'score': score_percent,
        'grade': check_student_grade(score_percent),
        'correct_count': correct_count,
        'total': total_questions,
        'answers_review': answers_review,
        'time_taken': time_taken,
        'title': 'Exam Results',
    }

    return render(request, 'students/quiz-results.html', context)

@login_required(login_url='quiz:login')
def student_profile_view(request):

    user = request.user
    context = {
        'user': user,
        'title': 'Student Profile',
    }
    return render(request, 'students/student-profile.html', context)