from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings  # Import settings
from .models import Opportunity, Application, Company
from .forms import OpportunityForm, ApplicationForm, CompanyForm
from .filters import OpportunityFilter

def opportunity_list(request):
    opportunities = Opportunity.objects.filter(status='open')
    
    # Filtering
    opportunity_filter = OpportunityFilter(request.GET, queryset=opportunities)
    opportunities = opportunity_filter.qs
    
    # Pagination
    paginator = Paginator(opportunities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter': opportunity_filter,
    }
    return render(request, 'opportunities/opportunity_list.html', context)

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(
            student=request.user, opportunity=opportunity
        ).exists()
    
    context = {
        'opportunity': opportunity,
        'has_applied': has_applied,
    }
    return render(request, 'opportunities/opportunity_detail.html', context)

@login_required
def apply_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    
    if Application.objects.filter(student=request.user, opportunity=opportunity).exists():
        messages.warning(request, 'You have already applied for this opportunity.')
        return redirect('opportunity_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.opportunity = opportunity
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('opportunity_detail', pk=pk)
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'opportunity': opportunity,
    }
    return render(request, 'opportunities/apply.html', context)

@login_required
def dashboard(request):
    student_profile = None
    applications = None
    
    # Check if user has a student profile
    if hasattr(request.user, 'studentprofile'):
        student_profile = request.user.studentprofile
        applications = Application.objects.filter(student=request.user)
    
    context = {
        'student_profile': student_profile,
        'applications': applications,
    }
    return render(request, 'opportunities/dashboard.html', context)

# Admin/Company views
@user_passes_test(lambda u: u.is_staff)
def manage_opportunities(request):
    opportunities = Opportunity.objects.all()
    context = {'opportunities': opportunities}
    return render(request, 'opportunities/manage_opportunities.html', context)

@user_passes_test(lambda u: u.is_staff)
def add_opportunity(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity added successfully!')
            return redirect('manage_opportunities')
    else:
        form = OpportunityForm()
    
    context = {'form': form}
    return render(request, 'opportunities/add_opportunity.html', context)
def opportunity_list(request):
    opportunities = Opportunity.objects.filter(status='open')
    
    # Filtering
    opportunity_filter = OpportunityFilter(request.GET, queryset=opportunities)
    opportunities = opportunity_filter.qs
    
    # Pagination
    paginator = Paginator(opportunities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate application counts for students
    application_counts = {}
    if request.user.is_authenticated and hasattr(request.user, 'user_type') and request.user.user_type == 'student':
        applications = request.user.application_set.all()
        application_counts = {
            'total': applications.count(),
            'pending': applications.filter(status='pending').count(),
        }
    
    context = {
        'page_obj': page_obj,
        'filter': opportunity_filter,
        'application_counts': application_counts,
    }
    return render(request, 'opportunities/opportunity_list.html', context)