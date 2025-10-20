from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
            ('admin', 'Admin'),
            ('teacher', 'Teacher'),
            ('student', 'Student'),
        )
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    username = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return self.username
    
class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Class(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return f'{self.name} class is headed by {self.teacher.user.first_name} {self.teacher.user.last_name}'
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.user.username

    # Performance helper methods used by the student views / templates
    def quizzes_taken(self):
        """Return a QuerySet of Attempts for this student."""
        return Attempt.objects.filter(student=self)

    def total_quizzes_taken(self):
        return self.quizzes_taken().count()

    def average_score(self):
        attempts = self.quizzes_taken().filter(is_completed=True)
        if not attempts.exists():
            return None
        # avoid division by zero
        total = sum(a.score for a in attempts)
        return round(total / attempts.count())

    def subjects_covered_count(self):
        # subjects from completed attempts
        attempts = self.quizzes_taken().filter(is_completed=True).select_related('quiz__subject')
        subject_ids = set(a.quiz.subject_id for a in attempts)
        return len(subject_ids)

    def subject_performance(self):
        """
        Returns a list of dicts with per-subject performance metrics:
        [{ 'subject': Subject instance, 'average_score': int, 'quizzes_taken': int, 'last_attempt': date }, ...]
        """
        from django.db.models import Avg, Max, Count

        completed_attempts = self.quizzes_taken().filter(is_completed=True).select_related('quiz__subject')
        # Aggregate per subject
        perf = {}
        for a in completed_attempts:
            subj = a.quiz.subject
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
                # compare last attempt by pk (not ideal but simple)
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
    
    
class Subject(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name
    
class SubjectClass(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classname = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject.name} for {self.classname.name}'

class Quiz(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    quizclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    max_score = models.IntegerField()
    start_time = models.DateField()
    end_time = models.DateField()
    duration = models.DurationField()
    date_created = models.DateField()

    # Calculate the quiz duration
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time and not self.duration:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(models.Model):
    question_text = models.CharField(max_length=255, null=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return self.question_text

class MultipleChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Attempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz.title

class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    multiple_choice = models.ForeignKey(MultipleChoice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Question: {self.question.question_text}. Answer: {self.multiple_choice.choice_text}. Correct: {self.is_correct}.'