from django.db import models
from django.contrib.auth.models import AbstractUser
from teachers.models import TeacherSubjectClass

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
            ('admin', 'Admin'),
            ('teacher', 'Teacher'),
            ('student', 'Student'),
        )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    username = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')

    # return full name of the user
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Class(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # Performance helper methods used by the student views / templates
    def quizzes_taken(self):
        """Return a QuerySet of Attempts for this student."""
        return Attempt.objects.filter(student=self)

    # total quizzes taken
    def total_quizzes_taken(self):
        return self.quizzes_taken().count()

    # average score across all completed attempts
    def average_score(self):
        attempts = self.quizzes_taken().filter(is_completed=True)
        if not attempts.exists():
            return None
        # avoid division by zero
        total = sum(a.score for a in attempts)
        return round(total / attempts.count())

    # number of subjects covered
    def subjects_covered_count(self):
        # subjects from completed attempts
        attempts = self.quizzes_taken().filter(is_completed=True).select_related('quiz__teacher_subject_class__subject_teacher__subject')
        subject_ids = set(a.quiz.teacher_subject_class.subject_teacher.subject_id for a in attempts)
        return len(subject_ids)

    def subject_performance(self):
        """
        Returns a list of dicts with per-subject performance metrics:
        [{ 'subject': Subject instance, 'average_score': int, 'quizzes_taken': int, 'last_attempt': date }, ...]
        """
        from django.db.models import Avg, Max, Count

        completed_attempts = self.quizzes_taken().filter(is_completed=True).select_related('quiz__teacher_subject_class__subject_teacher__subject')
        # Aggregate per subject
        perf = {}
        for a in completed_attempts:
            subj = a.quiz.teacher_subject_class.subject_teacher.subject
            sid = subj.id
            entry = perf.get(sid)
            if not entry:
                perf[sid] = {
                    'subject': subj,
                    'total_score': a.score,
                    'count': 1,
                    'last_attempt': a
                }
            else:
                entry['total_score'] += a.score
                entry['count'] += 1
                # compare last attempt by pk
                if a.pk and a.pk > getattr(entry['last_attempt'], 'pk', 0):
                    entry['last_attempt'] = a

        results = []
        for v in perf.values():
            avg = round(v['total_score'] / v['count']) if v['count'] else None
            last_date = getattr(v['last_attempt'], 'quiz', None)
            # last_attempt date should be the date the attempt was created; Attempt doesn't have date field - try to use quiz.date_created
            last_attempt_date = None
            if getattr(v['last_attempt'], 'quiz', None):
                last_attempt_date = v['last_attempt'].quiz.date_created

            results.append({
                'subject': v['subject'],
                'average_score': avg,
                'quizzes_taken': v['count'],
                'last_attempt': last_attempt_date,
            })

        return results
    
    # get enrolled subjects for this student with teachers name
    def get_enrolled_subjects(self):
        from django.db.models import Q
        return Subject.objects.filter(
            Q(subjectclass__classname=self.class_enrolled) &
            Q(subjectclass__studentsubject__student=self)
        ).distinct()

    def get_enrolled_subjects_with_teacher(self):
        """
        Return a list of dicts for the subjects the student is enrolled in along with the assigned teacher
        for this student's class (if any):
        [{ 'subject': Subject instance, 'teacher': Teacher instance or None }, ...]
        """
        from django.db.models import Q
        subjects = Subject.objects.filter(
            Q(subjectclass__classname=self.class_enrolled) &
            Q(subjectclass__studentsubject__student=self)
        ).distinct()

        results = []
        for subj in subjects:
            # find a TeacherSubjectClass linking this subject to this student's class
            tsc = TeacherSubjectClass.objects.filter(classname=self.class_enrolled,
                                                    subject_teacher__subject=subj).select_related('subject_teacher__teacher').first()
            teacher = None
            if tsc and getattr(tsc, 'subject_teacher', None):
                teacher = tsc.subject_teacher.teacher
            results.append({'subject': subj, 'teacher': teacher})

        return results

    # get full name of the student
    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    # get quizzes for this student
    # it returns all quizzes for the subjects the student is enrolled in
    # it uses the studentSubject model to filter quizzes by subject class
    # it returns a QuerySet of Quiz objects
    # it is used in the student dashboard to show quizzes for the subjects the student is enrolled in
    # filter the results using the subject class and the student subjects enrolled
    def get_quizzes(self):
        from django.db.models import Q
        return Quiz.objects.filter(
            Q(teacher_subject_class__classname=self.class_enrolled) &
            Q(teacher_subject_class__subject_teacher__subject__subjectclass__studentsubject__student=self)
        ).distinct()
    
    # get number of quizzes for this student
    def quizzes_count(self):
        return self.get_quizzes().count()

class Subject(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name
    
    # get classes for this subject
    def get_classes(self):
        from django.db.models import Q
        return Class.objects.filter(
            Q(subjectclass__subject=self)
        ).distinct()
    
class SubjectClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classname = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject.name} for {self.classname.name}'
    
    # get students enrolled in this subject class
    def get_students(self):
        from django.db.models import Q
        return Student.objects.filter(
            Q(class_enrolled=self.classname) &
            Q(studentsubject__class_subject=self)
        ).distinct()
    
    # get number of students enrolled in this subject class
    def students_count(self):
        return self.get_students().count()
    
class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_subject = models.ForeignKey(SubjectClass, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.get_full_name()} enrolled in {self.class_subject.subject.name} for {self.class_subject.classname.name}'
    
    # get quizzes for this student subject
    def get_quizzes(self):
        return Quiz.objects.filter(teacher_subject_class__classname=self.class_subject.classname,
                                   teacher_subject_class__subject_teacher__subject=self.class_subject.subject)
    
    # get number of quizzes for this student subject
    def quizzes_count(self):
        return self.get_quizzes().count()
    
class Quiz(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255)
    teacher_subject_class = models.ForeignKey(TeacherSubjectClass, on_delete=models.SET_NULL, null=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    start_date = models.DateTimeField(help_text='Start date and time for the quiz')
    due_date = models.DateTimeField(help_text='Due date for the quiz')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # get class for this quiz
    @property
    def quizclass(self):
        return self.teacher_subject_class.classname
    
    # get subject for this quiz
    @property
    def subject(self):
        return self.teacher_subject_class.subject_teacher.subject
    
    # get teacher for this quiz
    @property
    def teacher(self):
        return self.teacher_subject_class.subject_teacher.teacher
    
    # calculate quiz results
    def calculate_results(self):
        attempts = self.get_attempts().filter(is_completed=True)
        if not attempts.exists():
            return None
        total_score = sum(a.score for a in attempts)
        average_score = round(total_score / attempts.count())
        return {
            'total_score': total_score,
            'total_questions': self.questions_count(),
            'total_attempts': attempts.count(),
            'average_score': average_score, 
        }

    # get attempts for this quiz
    def get_attempts(self):
        return Attempt.objects.filter(quiz=self)
    
    # get number of attempts for this quiz
    def attempts_count(self):
        return self.get_attempts().count()
    
    # get number of completed attempts for this quiz
    def completed_attempts_count(self):
        return self.get_attempts().filter(is_completed=True).count()
    
    # get average score for this quiz
    def average_score(self):
        completed_attempts = self.get_attempts().filter(is_completed=True)
        if not completed_attempts.exists():
            return None
        total = sum(a.score for a in completed_attempts)
        return round(total / completed_attempts.count())
    
    # get questions for this quiz
    def get_questions(self):
        return Question.objects.filter(quiz=self)
    
    # get number of questions for this quiz
    def questions_count(self):
        return self.get_questions().count()
    
    # get questions and its multiple choices for this quiz
    def get_questions_with_choices(self):
        questions = self.get_questions()
        result = []
        for question in questions:
            choices = MultipleChoice.objects.filter(question=question)
            result.append({
                'question': question,
                'choices': choices
            })
        return result
    
    # increment_correct_answers
    def increment_correct_answers(self):
        self.correct_answers += 1
        self.save()

    # increment_total_answered
    def increment_total_answered(self):
        self.total_answered += 1
        self.save()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    question_text = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.question_text

class MultipleChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    choice_text = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
    
    # get question for this multiple choice
    @property
    def get_question(self):
        return self.question
    
    # get quiz for this multiple choice
    @property
    def get_quiz(self):
        return self.question.quiz

class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz.title
    
    # get student for this attempt
    @property
    def get_student(self):
        return self.student
    
    # get quiz for this attempt
    @property
    def get_quiz(self):
        return self.quiz
    
    # get answers for this attempt
    def get_answers(self):
        return AttemptAnswer.objects.filter(attempt=self)
    
    # get the correct answer for this attempt
    def get_correct_answers(self):
        return AttemptAnswer.objects.filter(attempt=self, is_correct=True)

class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    multiple_choice = models.ForeignKey(MultipleChoice, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Question: {self.question.question_text}. Answer: {self.multiple_choice.choice_text}. Correct: {self.is_correct}.'
    
    # get attempt for this answer
    @property
    def get_attempt(self):
        return self.attempt
    
    # get question for this answer
    @property
    def get_question(self):
        return self.question
    

