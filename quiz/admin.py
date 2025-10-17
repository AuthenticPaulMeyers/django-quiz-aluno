from django.contrib import admin
from .models import Class, ClassEnrollment, Teacher, CustomUser, Student, Attempt, AttemptAnswer, Question, Quiz, MultipleChoice, Subject

# Register your models here.
admin.site.register(Class)
admin.site.register(ClassEnrollment)
admin.site.register(Teacher)
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Attempt)
admin.site.register(AttemptAnswer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(MultipleChoice)
admin.site.register(Subject)