from django.urls import path
from .views import CustomTokenObtainPairView,CustomTokenRefreshView

urlpatterns = [    
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),    
]
