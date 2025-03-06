from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('login/', views.login_view, name='login'),  # Убедись, что name='login'
    path('logout/', views.logout_view, name='logout'),
]