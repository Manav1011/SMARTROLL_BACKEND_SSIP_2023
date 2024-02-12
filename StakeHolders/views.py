from asyncio import exceptions
from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)
from Profile.models import Profile
from rest_framework.decorators import api_view
from .models import Admin,Teacher,Student
from .serializers import AdminSerializer, TeacherSerializer,StudentSerializer
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
                token['obj'] = admin_serializer.data  

            if user.role == 'teacher':                
                teacher_obj = Teacher.objects.get(profile=user)
                teacher_serialized = TeacherSerializer(teacher_obj,many=False)
                token['obj'] = teacher_serialized.data  

            if user.role == 'student':                
                student_obj = Student.objects.get(profile=user)
                student_serialized = StudentSerializer(student_obj,many=False)
                token['obj'] = student_serialized.data  
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
@api_view(['POST'])
def student_register(request): 
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.data
        if 'email' in body and 'password' in body and 'enrollment' in body:
            student_obj = Student.objects.filter(enrollment=body['enrollment']).first()
            if student_obj:
                profile_obj = student_obj.profile
                if not profile_obj.is_active:
                    profile_obj.email = body['email']
                    profile_obj.set_password(body['password'])
                    profile_obj.is_active = True
                    profile_obj.save()
                    data['data'] = {'status':True}
                    return JsonResponse(data, status=200)
                else:
                    raise Exception("This student account is already active")
            else:
                raise Exception('This Student is not added')
        else:
            raise Exception('Credentials are not provided')
    except Exception as e:
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data, status=500)