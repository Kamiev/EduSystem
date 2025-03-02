from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Новая главная страница
    path('courses/', views.course_list, name='course_list'),
]