from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunity/<int:pk>/apply/', views.apply_opportunity, name='apply_opportunity'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin routes
    path('manage/', views.manage_opportunities, name='manage_opportunities'),
    path('manage/add/', views.add_opportunity, name='add_opportunity'),
]

# Remove the profile/edit URL from here since it belongs to users app