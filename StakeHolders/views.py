from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)
from rest_framework.decorators import api_view
from .models import Admin,Teacher,Student
from .serializers import AdminSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):        
        token = super().get_token(user)
        if user:            
            if user.role == 'admin':                
                admin_obj = Admin.objects.get(profile=user)
                admin_serializer = AdminSerializer(admin_obj,many=False)
                print(admin_serializer.data)
                token['admin_obj'] = admin_serializer.data        
            if user.role == 'student':                
                student_obj = Student.objects.get(profile=user)                
        return token


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token_authenticity(request):
    '''
    ## Check Token Authenticity

    **Path:** `/auth/api/check_token_authenticity`

    **Method:** `GET`

    **Authorization:** Token-based (Authentication required)

    ### Description
    Check the authenticity of the authentication token.

    ### Permissions
    - Requires user to be authenticated.

    ### Response
    - **Status Code:** 200 OK
    - **Content:**
    ```json
    {
        "data": true
    }
    ```
    Indicates that the token is authentic.

    ### Error Response
    - **Status Code:** 401 Unauthorized
    ```json
    {
        "detail": "Authentication credentials were not provided."
    }
    ```
    Indicates that the request lacks proper authentication credentials.

    ---

    *Note: Make sure to include the authentication token in the request header when accessing this endpoint.*
    '''
    return JsonResponse({'data':True},status=200)

    
class CustomTokenObtainPairView(TokenObtainPairView):
    """    
    # Allowed Method - POST
    #### Input:
    - `param1`: email.
    - `param2`: password.

    #### Output:
    `if user exists`
    - access token, refresh token.    
    
    `if user does not exists`
    - Response status code will be another than 200.
    """    
    serializer_class = CustomTokenObtainPairSerializer    

class CustomTokenRefreshView(TokenRefreshView):
    """    
    # Allowed Method - POST
    #### Input:
    - `param1`: refresh token.    

    #### Output:
    - `If refresh token is valid `: new access token, new refresh token.
    - `If refresh token is not valid`: Response status code will be another than 200.
    """        
