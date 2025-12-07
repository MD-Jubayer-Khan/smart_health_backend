from django.urls import path
from .views import suggestions, get_health_info

urlpatterns = [
    path('suggestions/', suggestions, name='suggestions'),
    path('health-info/', get_health_info, name='health-info'),

]
