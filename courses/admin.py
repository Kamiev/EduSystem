from django.contrib import admin
from .models import User, Course, Assignment, Grade, Attendance

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('FIO', 'email', 'role', 'login')  # Убери ссылки на groups и user_permissions
    list_filter = ('role',)
    search_fields = ('FIO', 'email', 'login')
    ordering = ('FIO',)  # Сортировка по FIO вместо username

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'start_date', 'end_date')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'score', 'comment')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')