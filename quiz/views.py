from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'students/index.html')
    
def academic(request):
    return render(request, 'students/policies/academic.html')

def privacy(request):
    return render(request, 'students/policies/privacy.html')