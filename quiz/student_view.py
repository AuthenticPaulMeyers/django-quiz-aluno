from django.shortcuts import render, redirect

def student_dashboard_view(request):
    return render(request, 'students/student-dashboard.html')

def all_quizzes_view(request):
    return render(request, 'students/view-all-quizzes.html')

def quiz_history_view(request):
    return render(request, 'students/quiz-history.html')

def quiz_details_view(request):
    return render(request, 'students/quiz-details.html')

def attempt_quiz_view(request):
    return render(request, 'students/quiz-page.html')

def quiz_results_view(request):
    return render(request, 'students/quiz-results.html')

def student_profile_view(request):
    return render(request, 'students/quiz-history.html')


