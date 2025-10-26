from django.shortcuts import render, redirect
from .models import Quiz, Student, Question, Attempt, MultipleChoice, AttemptAnswer
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

        # exclude quizzes already completed by this student (consider them 'expired' for this student)
        def not_completed_by_student(q):
            return not Attempt.objects.filter(student=student_obj, quiz=q, is_completed=True).exists()

        active_quizzes = [quiz for quiz in all_quizzes if quiz.start_date <= current_time <= quiz.due_date and not_completed_by_student(quiz)]

        upcoming_quizzes = [quiz for quiz in all_quizzes if quiz.start_date > current_time and not_completed_by_student(quiz)]

        # expired_quizzes: those past due OR quizzes already completed by this student
        expired_quizzes = [quiz for quiz in all_quizzes if quiz.due_date < current_time or Attempt.objects.filter(student=student_obj, quiz=quiz, is_completed=True).exists()]

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
            messages.info(request, 'You do not have quiz history.')
            return redirect('quiz:all-quizzes')

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
            return redirect('quiz:student-dashboard')

        # overall metrics
        avg_score = student_obj.average_score()
        quizzes_taken = student_obj.total_quizzes_taken()
        subjects_count = student_obj.subjects_covered_count()
        subject_perf = student_obj.subject_performance()

        # Get all attempts for this student so we can display grade per quiz taken
        attempts = Attempt.objects.filter(student=student_obj).select_related('quiz').order_by('-id')

        context = {
            'user': user,
            'average_score': f"{avg_score}%" if avg_score is not None else '0',
            'quizzes_taken': quizzes_taken,
            'subjects_covered': subjects_count,
            'subject_performance': subject_perf,
            'attempts': attempts,
        }

        return render(request, 'students/quiz-history.html', context)

    except Exception as e:
        # for debugging purposes
        print('Error in quiz_history_view:', e)
        messages.error(request, 'Unable to load quiz history.')
        return redirect('quiz:student-dashboard')

@login_required(login_url='quiz:login')
def quiz_details_view(request, quiz_id):

    try:
        quiz = Quiz.objects.filter(pk=quiz_id).first()
        if quiz is None:
            messages.error(request, 'Quiz not found.')
            return redirect('quiz:student-dashboard')
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
        return redirect('quiz:student-dashboard')

@login_required(login_url='quiz:login')
def attempt_quiz_view(request, quiz_id):

    quiz = Quiz.objects.filter(pk=quiz_id).first()

    if quiz is None:
        messages.error(request, 'Quiz not found.')
        return redirect('quiz:student-dashboard')

    # Prevent re-attempt if student already completed this quiz
    try:
        student_obj = request.user.student
    except Exception:
        messages.error(request, 'Student record not found.')
        return redirect('quiz:student-dashboard')

    existing = Attempt.objects.filter(student=student_obj, quiz=quiz, is_completed=True).first()
    if existing:
        messages.info(request, 'You have already completed this quiz. Viewing results instead.')
        return redirect('quiz:quiz-results', quiz_id=quiz.id)

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
    # Process POSTed answers and compute results
    quiz = Quiz.objects.filter(pk=quiz_id).first()
    if quiz is None:
        messages.error(request, 'Quiz not found.')
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
                'score': f"{existing_attempt.score}%",
                'correct_count': correct_count,
                'total': answers.count(),
                'answers_review': answers_review,
                'time_taken': None,
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
            'score': f"{existing_attempt.score}%",
            'correct_count': correct_count,
            'total': answers.count(),
            'answers_review': answers_review,
            'time_taken': None,
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

    context = {
        'score': f"{score_percent}%",
        'correct_count': correct_count,
        'total': total_questions,
        'answers_review': answers_review,
        'time_taken': time_taken,
    }

    return render(request, 'students/quiz-results.html', context)

@login_required(login_url='quiz:login')
def student_profile_view(request):

    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'students/student-profile.html', context)