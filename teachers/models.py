from django.db import models
from django.apps import apps
from django.conf import settings

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField('quiz.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def fullname(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    # get subjects taught by this teacher
    def get_subjects_class(self):
        from django.db.models import Q
        return TeacherSubjectClass.objects.filter(
            Q(subject_teacher__teacher=self)
        ).distinct()
    
    # get number of subjects taught by this teacher
    def subjects_count(self):
        return self.get_subjects_class().count()
    
    # get classes taught by this teacher
    def get_classes(self):
        from django.db.models import Q
        Class = apps.get_model('quiz', 'Class')
        return Class.objects.filter(
            Q(teachersubjectclass__subject_teacher__teacher=self)
        ).distinct()
    
    # get number of classes taught by this teacher
    def classes_count(self):
        return self.get_classes().count()
    
    # get quizzes created by this teacher
    def get_quizzes(self):
        from django.db.models import Q
        Quiz = apps.get_model('quiz', 'Quiz')
        return Quiz.objects.filter(
            Q(teacher_subject_class__subject_teacher__teacher=self)
        ).distinct()
    
    # get number of quizzes created by this teacher
    def quizzes_count(self):
        return self.get_quizzes().count()
    
    # get students taught by this teacher
    def get_students(self):
        from django.db.models import Q
        Student = apps.get_model('quiz', 'Student')
        return Student.objects.filter(
            Q(class_enrolled__teachersubjectclass__subject_teacher__teacher=self)
        ).distinct()
    
    # get number of students taught by this teacher
    def students_count(self):
        return self.get_students().count()

class SubjectTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey('quiz.Subject', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher.fullname()} teaches {self.subject.name}'
    
class TeacherSubjectClass(models.Model):
    subject_teacher = models.ForeignKey(SubjectTeacher, on_delete=models.CASCADE)
    classname = models.ForeignKey('quiz.Class', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject_teacher.subject.name} - {self.classname.name}'
    
    # get quizzes for this teacher subject class
    def get_quizzes(self):
        from quiz.models import Quiz
        return Quiz.objects.filter(teacher_subject_class=self)
    
    # get number of quizzes for this teacher subject class
    def quizzes_count(self):
        return self.get_quizzes().count()
    
    # get students for this teacher subject class
    def get_students(self):
        from django.db.models import Q
        Student = apps.get_model('quiz', 'Student')
        return Student.objects.filter(
            Q(class_enrolled=self.classname) &
            Q(studentsubject__class_subject__subject=self.subject_teacher.subject)
        ).distinct()
    
    # get number of students for this teacher subject class
    def students_count(self):
        return self.get_students().count()
