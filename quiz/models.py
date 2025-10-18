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

class Student(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Teacher(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Class(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return f'{self.name} class is headed by {self.teacher.user.first_name} {self.teacher.user.last_name}'

class ClassEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classname = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.student.user.first_name} {self.student.user.last_name} enrolled in {self.classname.name}'

class Subject(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name 
    
class Quiz(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
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