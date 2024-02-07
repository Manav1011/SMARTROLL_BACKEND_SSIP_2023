from django.urls import path,include
from .views import get_object_counts
urlpatterns = [        
    path('get_object_counts',get_object_counts,name='get_object_counts'),    
]
