
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('quiz.urls')),
    path('teacher/', include('teachers.urls')),
]

handler404 = 'quiz.views.custom_page_not_found_view'
handler500 = 'quiz.views.custom_server_error_view'
