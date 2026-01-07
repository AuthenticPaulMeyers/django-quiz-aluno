from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'students/index.html')
    
def academic(request):
    return render(request, 'students/policies/academic.html')

def privacy(request):
    return render(request, 'students/policies/privacy.html')

# Render custom 404 page
def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
    
# Render custom 500 page
def custom_server_error_view(request):
    return render(request, '500.html', status=500)