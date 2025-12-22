from django import forms
from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm
from .models import CustomUser, Quiz, Question, MultipleChoice, TeacherSubjectClass

# Quiz Forms
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'teacher_subject_class', 'duration', 'start_date', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add quiz instructions...'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter quiz title'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Enter time allowed'}),
        }

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            # Filter teacher_subject_class choices to only show classes taught by this teacher
            self.fields['teacher_subject_class'].queryset = TeacherSubjectClass.objects.filter(
                subject_teacher__teacher=teacher
            )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'image']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3}),
            'image': forms.FileInput(),
        }

class MultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = MultipleChoice
        fields = ['choice_text', 'is_correct']

class StudentEditForm(forms.ModelForm):
    # expose user fields on the same form
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)

    class Meta:
        # import Student lazily to avoid circular import in some cases
        from .models import Student
        model = Student
        fields = ['class_enrolled']

    def __init__(self, *args, allowed_classes=None, **kwargs):
        # pop instance if present then call super
        super().__init__(*args, **kwargs)
        # limit classes to those allowed (teacher's classes) when provided
        if allowed_classes is not None:
            self.fields['class_enrolled'].queryset = allowed_classes

        # if instance provided, populate user fields
        instance = kwargs.get('instance')
        if instance and hasattr(instance, 'user'):
            self.fields['first_name'].initial = instance.user.first_name
            self.fields['last_name'].initial = instance.user.last_name
            self.fields['username'].initial = instance.user.username

    def save(self, commit=True):
        # save Student.class_enrolled via ModelForm save
        student = super().save(commit=False)

        # update related user fields
        user = student.user
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.username = self.cleaned_data.get('username', user.username)

        if commit:
            user.save()
            student.save()

        return student

# Login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, strip=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=30, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Change password form
class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=40, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    confirm_password = forms.CharField(max_length=40, strip=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

# Admin create user form
class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "role")

