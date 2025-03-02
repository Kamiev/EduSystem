from django.db import models

class User(models.Model):
    FIO = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # Хешировать позже

class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=15, choices=[('present', 'Present'), ('absent', 'Absent')])