from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Course

def login_view(request):
    if request.method == 'POST':
        login_field = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, login=login_field, password=password)
        if user is not None:
            login(request, user)
            return redirect('course_list')
        else:
            return render(request, 'courses/login.html', {'error': 'Invalid login or password'})
    return render(request, 'courses/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def course_list(request):
    courses = Course.objects.all()
    for course in courses:
        for section in course.coursesection_set.all():
            section.embedded_video_url = section.get_embedded_video_url()
    return render(request, 'courses/course_list.html', {'courses': courses})

def home(request):
    return render(request, 'courses/home.html', {'title': 'EduSystem Home'})