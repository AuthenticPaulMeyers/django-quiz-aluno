from django.contrib import admin
from .models import CustomUser, Teacher, Class, Student, Subject, SubjectClass, StudentSubject, SubjectTeacher, TeacherSubjectClass, Quiz, Question, MultipleChoice, Attempt, AttemptAnswer

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Branding
admin.site.site_header = "Aluno Quiz Admin"
admin.site.site_title = "Aluno Admin Portal"
admin.site.index_title = "Site administration"

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'gender', 'role', 'is_active']
    list_filter = ['role', 'gender', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'role']
    ordering = ['username']
    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('role',)}),
        ('User Gender', {'fields': ('gender',)}),
    )

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subjects_count', 'classes_count', 'quizzes_count', 'students_count']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['subjects_count', 'classes_count', 'quizzes_count', 'students_count']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'class_enrolled', 'total_quizzes_taken', 'average_score']
    list_filter = ['class_enrolled']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['total_quizzes_taken', 'average_score']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class SubjectClassAdmin(admin.ModelAdmin):
    list_display = ['subject', 'classname', 'students_count']
    search_fields = ['subject__name', 'classname__name']
    readonly_fields = ['students_count']

class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_subject', 'student__class_enrolled']
    list_filter = ['student__class_enrolled']
    search_fields = ['student__user__first_name', 'student__user__last_name']

class SubjectTeacherAdmin(admin.ModelAdmin):
    list_display = ['subject', 'teacher']
    search_fields = ['subject__name', 'subject_teacher__teacher__user__last_name']

class TeacherSubjectClassAdmin(admin.ModelAdmin):
    list_display = ['subject_teacher', 'classname', 'students_count', 'quizzes_count']
    readonly_fields = ['students_count', 'quizzes_count']

class MultipleChoiceInline(admin.TabularInline):
    model = MultipleChoice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz']
    search_fields = ['question_text', 'quiz__title']
    inlines = [MultipleChoiceInline]

class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'quizclass', 'teacher', 'duration', 'date_created', 'attempts_count', 'average_score']
    list_filter = ['teacher_subject_class__subject_teacher__subject', 'teacher_subject_class__classname', 'date_created']
    search_fields = ['title', 'teacher_subject_class__subject_teacher__teacher__user__first_name']
    readonly_fields = ['attempts_count', 'average_score']

class AttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'is_completed']
    list_filter = ['is_completed', 'quiz']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'quiz__title']

class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'multiple_choice', 'is_correct']

# Register models with their custom ModelAdmin classes
admin.site.register(Class)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentSubject, StudentSubjectAdmin)
admin.site.register(SubjectClass, SubjectClassAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(AttemptAnswer, AttemptAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(MultipleChoice)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectTeacher, SubjectTeacherAdmin)
admin.site.register(TeacherSubjectClass, TeacherSubjectClassAdmin)