from django.urls import path
from .views import CustomTokenObtainPairView,CustomTokenRefreshView,check_token_authenticity

urlpatterns = [    
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),    
    path('api/check_token_authenticity', check_token_authenticity, name='check_token_authenticity'),
]
