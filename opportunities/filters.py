import django_filters
from .models import Opportunity
     
class OpportunityFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
    company__name = django_filters.CharFilter(lookup_expr='icontains', label='Company name')
    opportunity_type = django_filters.ChoiceFilter(choices=Opportunity.OPPORTUNITY_TYPES)
    location = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Opportunity
        fields = ['title', 'company__name', 'opportunity_type', 'location']
