import logging
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)
from quiz.models import Quiz, Student, Question, Attempt, MultipleChoice, Class, Subject
from quiz.forms import QuizForm, StudentEditForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import TeacherSubjectClass

# Dashboard
@login_required(login_url='quiz:login')
def teacher_dashboard_view(request):
	# get the current logged in user
	user = request.user

	# First check if user has teacher role
	if user.role != 'teacher':
		messages.error(request, 'Access denied. You are not registered as a teacher.')
		return redirect('quiz:login')
	
	try:
		# get the teacher object
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
		current_time = timezone.localtime(timezone.now())

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
		logger.error(f"Error in teacher_dashboard_view: {e}")
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
		current_time = timezone.localtime(timezone.now())

		context={
				'user': user,
				'title': 'Dashboard',
				'quizzes': quizzes,
				'current_time': current_time,
				'quizzes_count': quizzes_count,
		}

		return render(request, 'teachers/all-quizzes.html', context)

	except Exception as e:
		logger.error(f"Error in all_quizzes_view: {e}")
		messages.error(request, 'An error occurred while accessing teacher profile.')
		return redirect('quiz:login')

#view classes
@login_required(login_url='quiz:login')
def students_view(request):
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

		# classes taught by this teacher
		tsc_qs = TeacherSubjectClass.objects.filter(subject_teacher__teacher=teacher_obj)
		classes_qs = Class.objects.filter(pk__in=tsc_qs.values_list('classname_id', flat=True)).distinct()

		# students in the teacher's classes
		students_qs = Student.objects.filter(class_enrolled__in=classes_qs).select_related('user', 'class_enrolled')

		# optional filter by class via GET param
		selected_class = request.GET.get('class')
		if selected_class:
			students_qs = students_qs.filter(class_enrolled__id=selected_class)

		students = students_qs.order_by('class_enrolled__name', 'user__last_name', 'user__first_name')
		students_count = students.count()

		context={
				'user': user,
				'title': 'Students',
				'students_count': students_count,
				'students': students,
				'classes': classes_qs,
				'selected_class': int(selected_class) if selected_class else None,
		}
		return render(request, 'teachers/students.html', context)
	
	except Exception as e:
		logger.error(f"Error fetching teacher data: {e}")
		messages.error(request, "Error fetching teacher data")
		return redirect("teachers:dashboard")

# Edit Student
@login_required(login_url='quiz:login')
def edit_student(request, student_id):
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

		# classes taught by this teacher
		tsc_qs = TeacherSubjectClass.objects.filter(subject_teacher__teacher=teacher_obj)
		allowed_classes = Class.objects.filter(pk__in=tsc_qs.values_list('classname_id', flat=True)).distinct()

		# load the student only if they belong to one of the teacher's classes
		student = Student.objects.select_related('user', 'class_enrolled').filter(pk=student_id, class_enrolled__in=allowed_classes).first()
		if not student:
			messages.error(request, 'Student not found or not in your classes.')
			return redirect('teachers:students')

		if request.method == 'POST':
			form = StudentEditForm(request.POST, instance=student, allowed_classes=allowed_classes)
			if form.is_valid():
				form.save()
				messages.success(request, 'Student updated successfully.')
				return redirect('teachers:students')
			else:
				messages.error(request, 'Please correct the errors below.')
		else:
			form = StudentEditForm(instance=student, allowed_classes=allowed_classes)

		context = {
			'user': user,
			'title': 'Edit Student',
			'form': form,
			'student': student,
		}
		return render(request, 'teachers/edit-student.html', context)

	except Exception as e:
		logger.error(f"Error editing student: {e}")
		messages.error(request, 'Error editing student')
		return redirect('teachers:students')

# Delete student
@login_required(login_url='quiz:login')
def delete_student(request, student_id):
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

		tsc_qs = TeacherSubjectClass.objects.filter(subject_teacher__teacher=teacher_obj)
		allowed_classes = Class.objects.filter(pk__in=tsc_qs.values_list('classname_id', flat=True)).distinct()

		student = Student.objects.select_related('user', 'class_enrolled').filter(pk=student_id, class_enrolled__in=allowed_classes).first()
		if not student:
			messages.error(request, 'Student not found or not in your classes.')
			return redirect('teachers:students')

		if request.method == 'POST':
			# deleting the user will cascade-delete Student because of OneToOne(on_delete=CASCADE)
			student.user.delete()
			messages.success(request, 'Student deleted successfully.')
			return redirect('teachers:students')

		# If reached by GET, redirect back (template delete form uses POST)
		return redirect('teachers:students')

	except Exception as e:
		logger.error(f"Error deleting student: {e}")
		messages.error(request, 'Error deleting student')
		return redirect('teachers:students')

#view reports
@login_required(login_url='quiz:login')
def reports_view(request):
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

        # Get all the classes and subjects taught by this teacher
        tsc_qs = TeacherSubjectClass.objects.filter(subject_teacher__teacher=teacher_obj)
        classes = Class.objects.filter(pk__in=tsc_qs.values_list('classname_id', flat=True)).distinct()
        subjects = Subject.objects.filter(pk__in=tsc_qs.values_list('subject_teacher__subject_id', flat=True)).distinct()

        # Get filter parameters
        selected_class = request.GET.get('class')
        selected_subject = request.GET.get('subject')
        
        # Base queryset for attempts
        attempts = Attempt.objects.filter(
            quiz__teacher_subject_class__subject_teacher__teacher=teacher_obj,
            is_completed=True
        ).select_related(
            'student__user',
            'student__class_enrolled',
            'quiz__teacher_subject_class__subject_teacher__subject'
        ).order_by('-quiz__date_created')

        # Apply filters
        if selected_class:
            attempts = attempts.filter(student__class_enrolled_id=selected_class)
        if selected_subject:
            attempts = attempts.filter(quiz__teacher_subject_class__subject_teacher__subject_id=selected_subject)

        if request.GET.get('download') == 'excel':
            import pandas as pd
            from django.http import HttpResponse
            from io import BytesIO
            
            # Convert attempts to dataframe
            data = []
            for attempt in attempts:
                data.append({
                    'Student Name': f"{attempt.student.user.first_name} {attempt.student.user.last_name}",
                    'Class': attempt.student.class_enrolled.name,
                    'Subject': attempt.quiz.subject.name,
                    'Quiz Title': attempt.quiz.title,
                    'Score': f"{attempt.score}%",
                    'Date': attempt.quiz.date_created.strftime('%Y-%m-%d'),
                })
            
            df = pd.DataFrame(data)
            
            # Create Excel file
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False, sheet_name='Quiz Reports')
            excel_file.seek(0)
            
            response = HttpResponse(
                excel_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=quiz_reports.xlsx'
            return response

        context = {
            'user': user,
            'title': 'Reports',
            'attempts': attempts,
            'classes': classes,
            'subjects': subjects,
            'selected_class': int(selected_class) if selected_class else None,
            'selected_subject': int(selected_subject) if selected_subject else None,
        }
        return render(request, 'teachers/reports.html', context)
    
    except Exception as e:
        logger.error(f"Error loading reports: {e}")
        messages.error(request, 'Error loading reports')
        return redirect('teachers:dashboard')

#view subjects
@login_required(login_url='quiz:login')
def subjects_view(request):
	user = request.user

	context={
		'user': user,
		'title': 'Subjects'
	}
	return render(request, 'teachers/subjects.html', context)

# Quiz details
@login_required(login_url='quiz:login')
def view_quiz_details(request, quiz_id):
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

		quiz = Quiz.objects.filter(pk=quiz_id).first()
		if quiz is None:
			messages.error(request, 'Quiz not found....')
			return redirect('teachers:dashboard')

		# ensure this quiz belongs to the teacher
		if quiz.teacher != teacher_obj:
			messages.error(request, 'Access denied. This quiz does not belong to you.')
			return redirect('teachers:all-quizzes')

		# POST handlers for edit actions
		if request.method == 'POST':
			action = request.POST.get('action')

			# Save quiz metadata
			if action == 'save_quiz':
				form = QuizForm(request.POST, instance=quiz, teacher=teacher_obj)
				if form.is_valid():
					q = form.save(commit=False)
					q.save()
					messages.success(request, 'Quiz updated successfully.')
				else:
					messages.error(request, 'Please correct the errors in the quiz form.')
				return redirect('teachers:quiz-details', quiz_id=quiz.id)

			# Delete entire quiz
			if action == 'delete_quiz':
				quiz.delete()
				messages.success(request, 'Quiz deleted successfully.')
				return redirect('teachers:all-quizzes')

			# Add a new blank question
			if action == 'add_question':
				q_text = request.POST.get('new_question_text', '').strip() or 'New question'
				new_q = Question.objects.create(quiz=quiz, question_text=q_text)
				# create 4 empty choices
				for _ in range(4):
					MultipleChoice.objects.create(question=new_q, choice_text='')
				messages.success(request, 'Question added.')
				return redirect('teachers:quiz-details', quiz_id=quiz.id)

			# Save edits to a question and its choices
			if action == 'save_question':
				try:
					question_id = int(request.POST.get('question_id'))
				except Exception:
					messages.error(request, 'Invalid question id.')
					return redirect('teachers:quiz-details', quiz_id=quiz.id)

				question = Question.objects.filter(pk=question_id, quiz=quiz).first()
				if not question:
					messages.error(request, 'Question not found.')
					return redirect('teachers:quiz-details', quiz_id=quiz.id)

				# update question text
				q_text = request.POST.get(f'question_text_{question.id}', '').strip()
				if q_text:
					question.question_text = q_text
					question.save()

				# update choices
				choices = MultipleChoice.objects.filter(question=question)
				for choice in choices:
					new_text = request.POST.get(f'choice_text_{choice.id}', '').strip()
					is_corr = request.POST.get(f'is_correct_{choice.id}') == 'on'
					choice.choice_text = new_text
					choice.is_correct = bool(is_corr)
					choice.save()

				messages.success(request, 'Question updated.')
				return redirect('teachers:quiz-details', quiz_id=quiz.id)

			# Delete a question
			if action == 'delete_question':
				try:
					question_id = int(request.POST.get('question_id'))
				except Exception:
					messages.error(request, 'Invalid question id.')
					return redirect('teachers:quiz-details', quiz_id=quiz.id)

				question = Question.objects.filter(pk=question_id, quiz=quiz).first()
				if question:
					question.delete()
					messages.success(request, 'Question deleted.')
				else:
					messages.error(request, 'Question not found.')
				return redirect('teachers:quiz-details', quiz_id=quiz.id)

		# GET: prepare forms and question list
		quiz_form = QuizForm(instance=quiz, teacher=teacher_obj)
		questions = Question.objects.filter(quiz=quiz).order_by('id')
		# Prefetch choices per question for template efficiency
		choices_map = {}
		for q in questions:
			choices_map[q.id] = MultipleChoice.objects.filter(question=q).order_by('id')

		context = {
			'user': user,
			'title': 'Quiz Details',
			'quiz': quiz,
			'quiz_form': quiz_form,
			'questions': questions,
			'choices_map': choices_map,
		}

		return render(request, 'teachers/quiz-details.html', context)

	except Exception as e:
		messages.error(request, 'Quiz not found.')
		logger.error(f"Error in view_quiz_details: {e}")
		return redirect('teachers:dashboard')

# ToDo: Teacher profile
@login_required(login_url='quiz:login')
def teacher_profile_view(request):

    user = request.user
    context = {
        'user': user,
        'title': 'Teacher Profile',
    }
    return render(request, 'teachers/teacher-profile.html', context)

# Create quiz
@login_required(login_url='quiz:login')
def create_quiz_view(request):
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

		# Get teacher's subject classes for the form
		teacher_subject_classes = teacher_obj.get_subjects_class()
        
		if request.method == 'POST':
			quiz_form = QuizForm(request.POST, teacher=teacher_obj)
			if quiz_form.is_valid():
				# Save quiz but don't commit yet
				quiz = quiz_form.save(commit=False)
				quiz.date_created = timezone.localtime(timezone.now()).date()
				quiz.save()

				# Handle questions and choices
				questions_data = request.POST.getlist('question_text[]')
				choices_text = request.POST.getlist('choice_text[]')
				correct_answers = request.POST.getlist('is_correct[]')

				# Build per-question (text, image) pairs using indexed file inputs (question_image_0, question_image_1, ...)
				paired_questions = []
				for i, q_text in enumerate(questions_data):
					q_image = request.FILES.get(f'question_image_{i}') if request.FILES else None
					paired_questions.append((q_text, q_image))

				# Process questions
				created_any = False
				for i, (q_text, q_image) in enumerate(paired_questions):
					# Only process if question text is not empty
					if q_text and str(q_text).strip():
						question = Question.objects.create(
							quiz=quiz,
							question_text=q_text,
							image=q_image if q_image else None
						)

						# Create 4 choices for this question
						start_idx = i * 4
						for j in range(4):
							choice_idx = start_idx + j
							if choice_idx < len(choices_text):
								is_correct = str(choice_idx) in correct_answers
								MultipleChoice.objects.create(
									question=question,
									choice_text=choices_text[choice_idx],
									is_correct=is_correct
								)
						created_any = True

				# After processing all questions
				if created_any:
					messages.success(request, 'Quiz created successfully!')
					return redirect('teachers:all-quizzes')
				else:
					messages.error(request, 'Please correct the errors below.')

				context = {
					'user': user,
					'title': 'Create Quiz',
					'form': quiz_form,
					'teacher_subject_classes': teacher_subject_classes,
				}

			return render(request, 'teachers/create-quiz.html', context)
		else:
			quiz_form = QuizForm(teacher=teacher_obj)
			context = {
				'user': user,
				'title': 'Create Quiz',
				'form': quiz_form,
				'teacher_subject_classes': teacher_subject_classes,
			}
			return render(request, 'teachers/create-quiz.html', context)

	except Exception as e:
		logger.error(f"Failed to create quiz: {str(e)}")
		messages.error(request, "Failed to create quiz.")
		return redirect("teachers:all-quizzes")

# Delete quiz
@login_required(login_url='quiz:login')
def delete_quiz_view(request, quiz_id):
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
		# get the teacher subject class object fot this teacher
		teacher_subject_classes = TeacherSubjectClass.objects.filter(subject_teacher__teacher=teacher_obj)
		# load the quiz only if it belongs to this teacher
		quiz = Quiz.objects.filter(pk=quiz_id, teacher_subject_class__in=teacher_subject_classes).first()
		if quiz is None:
			messages.error(request, 'Quiz not found or does not belong to you.')
			return redirect('teachers:all-quizzes')
		# delete the quiz
		quiz.delete()
		messages.success(request, 'Quiz deleted successfully.')
		return redirect('teachers:all-quizzes')

	except Exception as e:
		logger.error(f"Error deleting quiz: {e}")
		messages.error(request, 'Error deleting quiz.')
		return redirect('teachers:all-quizzes')
	
# Enroll student to class subject
# Remove student from class subject enrolled (Drop subject)
# Download reports
