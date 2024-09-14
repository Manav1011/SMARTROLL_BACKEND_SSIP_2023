from asyncio import exceptions
from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)
from Profile.models import Profile
from rest_framework.decorators import api_view
from .models import Admin,Teacher,Student,SuperAdmin
from .serializers import AdminSerializer, TeacherSerializer,StudentSerializer,SuperAdminSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.conf import settings as django_settings
from django.core.mail import send_mail
from threading import Thread
import uuid,time

# Create your views here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

def send_forgot_password_mail(receiver,student_slug,host):    
    sender_email = django_settings.EMAIL_HOST_USER
    sent = False
    url = f'http://{host}/forgot_password/{student_slug}'
    try:
        send_mail('Reset Your Password',url, from_email=sender_email,recipient_list=[receiver])
        sent=True
    except Exception as e:             
        sent = False
    return sent

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):        
        token = super().get_token(user)
        if user:                        
            if user.role == 'superadmin':                
                admin_obj = SuperAdmin.objects.get(profile=user)
                admin_serializer = SuperAdminSerializer(admin_obj,many=False)
                token['obj'] = admin_serializer.data  

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
def forgot_password(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.data
        if 'enrollment' not in body:
            raise Exception('Parameters missing')
        student_obj = Student.objects.filter(enrollment=body['enrollment']).first()
        if not student_obj:
            raise Exception('Student does not exist')
        recipent_email = student_obj.profile.email
        student_obj.slug = generate_unique_hash()
        student_obj.save()
        Thread(target=send_forgot_password_mail,args=(recipent_email,student_obj.slug,request.META['HTTP_HOST'])).start()
        return JsonResponse(data, status=200)

    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data, status=500)

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
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data, status=500)