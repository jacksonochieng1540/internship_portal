from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('company', 'Company Representative'),
        ('admin', 'Administrator'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class StudentProfile(models.Model):
    # Use the custom user model
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    year_of_study = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    skills = models.CharField(max_length=300, blank=True)
    resume = models.FileField(upload_to='student_resumes/', blank=True, null=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class CompanyProfile(models.Model):
    # Use the custom user model
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    company = models.OneToOneField('opportunities.Company', on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company.name}"