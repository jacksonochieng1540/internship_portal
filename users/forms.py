from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, StudentProfile, CompanyProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    student_id = forms.CharField(max_length=20, required=True)
    course = forms.CharField(max_length=100, required=True)
    year_of_study = forms.IntegerField(min_value=1, max_value=6, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                 'student_id', 'course', 'year_of_study']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'student'
        if commit:
            user.save()
            student_profile = StudentProfile.objects.create(
                user=user,
                student_id=self.cleaned_data['student_id'],
                course=self.cleaned_data['course'],
                year_of_study=self.cleaned_data['year_of_study']
            )
        return user

class CompanyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    company_name = forms.CharField(max_length=200, required=True)
    position = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                 'company_name', 'position']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        if commit:
            user.save()
            # Note: Company object should be created separately or this form should be extended
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'course', 'year_of_study', 'skills', 'resume', 
                 'linkedin_profile', 'github_profile']