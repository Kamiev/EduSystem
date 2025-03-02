from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def home(request):
    return render(request, 'courses/home.html', {'title': 'EduSystem Home'})