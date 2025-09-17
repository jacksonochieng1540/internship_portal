from django import template
from opportunities.models import Application

register = template.Library()

@register.filter
def has_applied(opportunity, user):
    """Check if a user has applied to an opportunity"""
    if not user.is_authenticated:
        return False
    return Application.objects.filter(opportunity=opportunity, student=user).exists()

@register.filter
def filter_by_status(applications, status):
    """Filter applications by status"""
    return applications.filter(status=status)