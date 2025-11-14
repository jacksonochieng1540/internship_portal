from django.contrib import admin
from .models import Opportunity, Application, Company
from django.conf import settings  

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):  
    list_display = ['title', 'company', 'opportunity_type', 'status', 'application_deadline']
    list_filter = ['status', 'opportunity_type', 'created_at']
    search_fields = ['title', 'company__name']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'opportunity', 'status', 'application_date']
    list_filter = ['status', 'application_date']
    search_fields = ['student__username', 'opportunity__title']

admin.site.register(Company)
