from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, CompanyRegistrationForm, UserUpdateForm, StudentProfileUpdateForm
from .models import StudentProfile
from django.contrib.auth import logout
from django.shortcuts import redirect

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully!')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'users/register_student.html', {'form': form})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Company creation would happen here
            login(request, user)
            messages.success(request, f'Account created successfully!')
            return redirect('dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'users/register_company.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if hasattr(request.user, 'studentprofile'):
            p_form = StudentProfileUpdateForm(request.POST, request.FILES, 
                                            instance=request.user.studentprofile)
        else:
            p_form = None
            
        if u_form.is_valid() and (p_form is None or p_form.is_valid()):
            u_form.save()
            if p_form:
                p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if hasattr(request.user, 'studentprofile'):
            p_form = StudentProfileUpdateForm(instance=request.user.studentprofile)
        else:
            p_form = None

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        # If the user doesn't have a student profile, redirect to create one
        messages.info(request, 'Please complete your student profile first.')
        return redirect('profile')
    
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = StudentProfileUpdateForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login') 
    else:
        return render(request, 'users/logout_confirm.html')