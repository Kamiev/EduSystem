from django.contrib import admin
from .models import User, Course, Assignment, Grade, Attendance, MaterialLibrary, CourseSection

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('FIO', 'email', 'role', 'login')
    list_filter = ('role',)
    search_fields = ('FIO', 'email', 'login')
    ordering = ('FIO',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'start_date', 'end_date')

@admin.register(MaterialLibrary)
class MaterialLibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_locked', 'file', 'link', 'video_embed', 'content_text', 'photo')
    list_filter = ('is_locked',)
    search_fields = ('title', 'content_text')

@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'order', 'library_material', 'custom_content_text')
    list_filter = ('course',)
    search_fields = ('title', 'custom_content_text')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'score', 'comment')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')