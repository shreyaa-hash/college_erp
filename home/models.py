from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="0000000000")
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # AI Digital Twin Parameters
    github_profile = models.URLField(max_length=200, blank=True, null=True)
    study_hours_per_day = models.FloatField(default=3.0, help_text="Average study hours per day")
    coding_hours_per_week = models.FloatField(default=10.0, help_text="Average coding hours per week")
    communication_score = models.IntegerField(default=5, help_text="Communication skill rating (1-10)")
    stress_rating = models.IntegerField(default=5, help_text="Self-reported stress level (1-10)")
    
    # Career Targets
    dream_company = models.CharField(max_length=100, default="Google")
    target_package = models.FloatField(default=12.0, help_text="Target placement package in LPA")
    target_cgpa = models.FloatField(default=8.5)
    
    # Workload Metrics
    assignments_completed = models.IntegerField(default=8)
    total_assignments = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    faculty_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="Computer Science")

    def __str__(self):
        return f"{self.name} ({self.faculty_id})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    subject = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.date} - {self.status}"

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=100)
    marks = models.IntegerField(help_text="Marks obtained")
    total_marks = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.marks}/{self.total_marks}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    time = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

class Timetable(models.Model):
    day = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    time = models.CharField(max_length=50)
    faculty = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.day} - {self.subject} ({self.time})"