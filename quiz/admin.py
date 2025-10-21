from django.contrib import admin
from .models import CustomUser, Teacher, Class, Student, Subject, SubjectClass, StudentSubject, SubjectTeacher, TeacherSubjectClass, Quiz, Question, MultipleChoice, Attempt, AttemptAnswer

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('role',)}),
    )
    
# Register your models here.
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(StudentSubject)
admin.site.register(SubjectClass)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Attempt)
admin.site.register(AttemptAnswer)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(MultipleChoice)
admin.site.register(Subject)
admin.site.register(SubjectTeacher)
admin.site.register(TeacherSubjectClass)