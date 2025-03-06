from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    FIO = models.CharField(max_length=50, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    ], verbose_name="Role")
    login = models.CharField(max_length=50, unique=True, verbose_name="Login")
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_user_permissions')

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['FIO', 'email', 'role']

    def __str__(self):
        return f"{self.FIO} ({self.role})"

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Course Title")
    code = models.CharField(max_length=10, unique=True, verbose_name="Access Code")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    def __str__(self):
        return self.title

class MaterialLibrary(models.Model):
    title = models.CharField(max_length=100, verbose_name="Material Title")
    file = models.FileField(upload_to='material_library/', blank=True, null=True, verbose_name="Uploaded File")
    link = models.URLField(max_length=200, blank=True, null=True, verbose_name="External Link")
    video_embed = models.URLField(max_length=200, blank=True, null=True, verbose_name="Video Embed URL (e.g. YouTube)")
    content_text = models.TextField(blank=True, null=True, verbose_name="Content Text")
    photo = models.ImageField(upload_to='material_photos/', blank=True, null=True, verbose_name="Photo")
    is_locked = models.BooleanField(default=True, verbose_name="Locked (Uneditable)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.title} (Locked: {self.is_locked})"

class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    title = models.CharField(max_length=100, verbose_name="Section Title", blank=True)
    library_material = models.ForeignKey(MaterialLibrary, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Linked Library Material")
    custom_content_text = models.TextField(blank=True, null=True, verbose_name="Custom Text")
    custom_photo = models.ImageField(upload_to='course_photos/', blank=True, null=True, verbose_name="Custom Photo")
    custom_link = models.URLField(max_length=200, blank=True, null=True, verbose_name="Custom Link")
    custom_video_embed = models.URLField(max_length=200, blank=True, null=True, verbose_name="Custom Video Embed URL")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - Section {self.order}"

    def save(self, *args, **kwargs):
        if self.library_material and not self.custom_content_text and not self.custom_photo and not self.custom_link and not self.custom_video_embed:
            self.custom_content_text = self.library_material.content_text
            self.custom_photo = self.library_material.photo
            self.custom_link = self.library_material.link
            self.custom_video_embed = self.library_material.video_embed
        super().save(*args, **kwargs)

    def get_embedded_video_url(self):
        return self.custom_video_embed

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    title = models.CharField(max_length=100, verbose_name="Assignment Title")
    description = models.TextField(verbose_name="Description")
    deadline = models.DateTimeField(verbose_name="Deadline")

    def __str__(self):
        return self.title

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, verbose_name="Student")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Assignment")
    score = models.IntegerField(default=0, verbose_name="Score")
    comment = models.TextField(blank=True, verbose_name="Comment")

    def __str__(self):
        return f"{self.student.FIO} - {self.score}"

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    date = models.DateField(verbose_name="Date")
    status = models.CharField(max_length=15, choices=[('present', 'Present'), ('absent', 'Absent')], verbose_name="Status")

    def __str__(self):
        return f"{self.student.FIO} - {self.date} ({self.status})"