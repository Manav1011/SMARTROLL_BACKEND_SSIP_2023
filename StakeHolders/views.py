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

# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):        
        token = super().get_token(user)
        if user:
            token['profile'] = {
                'email':user.email,
                'name':user.name,
                'role':user.role
            }                   
            if user.role == 'admin':                
                admin_obj = Admin.objects.get(profile=user)
                admin_serializer = AdminSerializer(admin_obj,many=False)
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
        
    except Exception as e:        
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
        student_obj.branch = branch_obj
        student_obj.steps = 3
        student_obj.save()
        # Now get the semester of active batches
        batch = branch_obj.batches.all().filter(active=True).first()
        semesters = batch.semesters.all().filter(status=True)        
        semesters_serialized = SemesterSerializer(semesters,many=True)
        data = {"data":True,"steps":student_obj.steps,'semesters':semesters_serialized.data}
        return JsonResponse(data,status=200)
    except Exception as e:        
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
