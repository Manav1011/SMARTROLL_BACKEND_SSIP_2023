from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)
from rest_framework.decorators import api_view
from .models import Admin,Teacher,Student
from Manage.models import Branch,Batch,Semester,Subject
from Manage.serializers import BranchSerializer,SemesterSerializer,SubjectSerializer
from .serializers import AdminSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import io
import base64

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

@api_view(['POST'])    
def SetStudentCreds1(request):
    try:
        body = request.data
        if 'enrollment' not in body:
            raise Exception('Provide all the parameters')
        student_obj = Student.objects.get(enrollment=body['enrollment'])        
        if student_obj.steps == 1 or student_obj.steps == 2:
            if student_obj.steps == 1:
                student_obj.steps = 2
                student_obj.save()
            branches = Branch.objects.all()
            branches_serialized = BranchSerializer(branches,many=True)    
            data = {"data":True,"steps":student_obj.steps,'branches':branches_serialized.data,'student_slug':student_obj.slug}
            return JsonResponse(data,status=200)        
        elif student_obj.steps == 3:
            branch_obj = student_obj.branch            
            branches_serialized = BranchSerializer(branch_obj)
            batch = branch_obj.batches.all().filter(active=True).first()
            semesters = batch.semesters.all().filter(status=True)        
            semesters_serialized = SemesterSerializer(semesters,many=True)
            data = {"data":True,"steps":student_obj.steps,'branch':branches_serialized.data,'student_slug':student_obj.slug,'semesters':semesters_serialized.data}
            return JsonResponse(data,status=200)
        elif student_obj.steps == 4:
            branch_obj = student_obj.branch
            branches_serialized = BranchSerializer(branch_obj)
            semester_obj = student_obj.semester   
            semesters_serialized = SemesterSerializer(semester_obj) 
            subjects = semester_obj.subjects.all()
            subjects_serialized = SubjectSerializer(subjects,many=True)
            data = {"data":True,"steps":student_obj.steps,'branch':branches_serialized.data,'student_slug':student_obj.slug,'semester':semesters_serialized.data,'subjects':subjects_serialized.data}
            return JsonResponse(data,status=200)
    
        elif student_obj.steps == 5:
            branch_obj = student_obj.branch
            branches_serialized = BranchSerializer(branch_obj)
            semester_obj = student_obj.semester   
            semesters_serialized = SemesterSerializer(semester_obj) 
            subjects = student_obj.subjects.all()
            subjects_serialized = SubjectSerializer(subjects,many=True)
            data = {"data":True,"steps":student_obj.steps,'branch':branches_serialized.data,'student_slug':student_obj.slug,'semester':semesters_serialized.data,'subjects':subjects_serialized.data}
            return JsonResponse(data,status=200)   
        elif student_obj.steps == 6:
            branch_obj = student_obj.branch
            branches_serialized = BranchSerializer(branch_obj)
            semester_obj = student_obj.semester   
            semesters_serialized = SemesterSerializer(semester_obj) 
            subjects = student_obj.subjects.all()
            subjects_serialized = SubjectSerializer(subjects,many=True)
            signature = student_obj.signature_link
            data = {"data":True,"steps":student_obj.steps,'branch':branches_serialized.data,'student_slug':student_obj.slug,'semester':semesters_serialized.data,'subjects':subjects_serialized.data,'signature':signature}
            return JsonResponse(data,status=200)            
        
    except Exception as e:     
        print(e)      
        data = {"data":str(e)}
        return JsonResponse(data,status=500)    
    
@api_view(['POST'])    
def SetStudentCreds2(request):
    try:
        body = request.data
        if 'branch_slug' not in body and 'student_slug' not in body:
            raise Exception('Provide all the parameters')
        student_obj = Student.objects.get(slug=body['student_slug'])
        branch_obj = Branch.objects.get(slug=body['branch_slug'])
        # Now get the semester of active batches
        batch = branch_obj.batches.all().filter(active=True).first()
        print(batch)
        if not batch:
            raise Exception('There are no active batches in this branch')
        semesters = batch.semesters.all().filter(status=True)
        print(semesters)
        if not semesters:
            raise Exception('There are no active semesters in this batch')
        student_obj.branch = branch_obj
        student_obj.steps = 3
        student_obj.save()
        semesters_serialized = SemesterSerializer(semesters,many=True)
        data = {"data":True,"steps":student_obj.steps,'semesters':semesters_serialized.data}
        return JsonResponse(data,status=200)
    except Exception as e:  
        print(e)         
        data = {"data":str(e)}
        return JsonResponse(data,status=500)    

@api_view(['POST'])    
def SetStudentCreds3(request):
    try:
        body = request.data
        if 'semester_slug' not in body and 'student_slug' not in body:
            raise Exception('Provide all the parameters')
        student_obj = Student.objects.get(slug=body['student_slug'])
        semester_obj = Semester.objects.get(slug=body['semester_slug'])
        student_obj.semester = semester_obj
        student_obj.steps = 4
        student_obj.save()
        # Now get the subjects of current semester        
        subjects = semester_obj.subjects.all()
        subjects_serialized = SubjectSerializer(subjects,many=True)
        data = {"data":True,"steps":student_obj.steps,'subjects':subjects_serialized.data}
        return JsonResponse(data,status=200)
    except Exception as e:     
        print(e)   
        data = {"data":str(e)}
        return JsonResponse(data,status=500)    

@api_view(['POST'])    
def SetStudentCreds4(request):
    try:
        body = request.data
        if 'subject_arr' not in body and 'student_slug' not in body:
            raise Exception('Provide all the parameters')
        student_obj = Student.objects.get(slug=body['student_slug'])        
        for i in body['subject_arr']:
            subject_obj = Subject.objects.get(slug=i)
            student_obj.subjects.add(subject_obj)
        student_obj.steps = 5
        student_obj.save()
        # Now get the subjects of current semester                
        data = {"data":True,"steps":student_obj.steps}
        return JsonResponse(data,status=200)
    except Exception as e:    
        print(e)       
        data = {"data":str(e)}
        return JsonResponse(data,status=500)    

def base64_to_grayscale(b64_image_url,student_slug):
    # Decode the Base64 string
    image_data = base64.b64decode(b64_image_url.split(',')[1])

    # Load the image using Pillow
    original_image = Image.open(io.BytesIO(image_data))

    # Convert the image to grayscale
    grayscale_image = original_image.convert('L')

    grayscale_image_io = io.BytesIO()
    grayscale_image.save(grayscale_image_io, format='PNG')
    file_storage_obj = FileSystemStorage()
    saved_file = file_storage_obj.save(f"{student_slug}.png", ContentFile(grayscale_image_io.getvalue()))
    file_url = file_storage_obj.url(saved_file)
    return file_url

@api_view(['POST'])    
def SetStudentCreds5(request):
    try:
        body = request.data
        if 'signatureb64' not in body and 'password' not in body and 'student_slug' not in body:
            raise Exception('Provide all the parameters')
        student_obj = Student.objects.get(slug=body['student_slug'])
        student_obj.steps = 6
        # Convert the signature to png and store it
        profile_obj = student_obj.profile
        signature_url = base64_to_grayscale(body['signatureb64'],body['student_slug'])
        student_obj.signature_link = signature_url
        student_obj.save()
        profile_obj.set_password(body['password'])
        profile_obj.save()
        # Now get the subjects of current semester                
        data = {"data":True,"steps":student_obj.steps,'signature':student_obj.signature_link}
        return JsonResponse(data,status=200)
    except Exception as e:  
        print(e)         
        data = {"data":str(e)}
        return JsonResponse(data,status=500)    


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
