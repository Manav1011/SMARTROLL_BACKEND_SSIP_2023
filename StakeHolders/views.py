from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,
)
from .models import Admin,Teacher
from .serializers import AdminSerializer

# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):        
        token = super().get_token(user)
        if user:
            token['email'] = user.email
            token['name'] = user.name            
            token['role'] = user.role
            if user.role == 'admin':                
                admin_obj = Admin.objects.get(profile=user)
                admin_serializer = AdminSerializer(admin_obj,many=False)
                # Admin exclusive fields will be here
                branch_obj = admin_obj.branch
                # Count the batches in particular branch - from branch
                batch_obj = branch_obj.batches.all()
                batches_count = batch_obj.count()
                # Count semesters in each batches - from batches
                semesters = []
                for i in batch_obj:
                    semesters_obj = i.semesters.all()
                    for j in semesters_obj:
                        semesters.append(j)
                semesters_count = len(semesters)
                # Count Subjects in each semesters - from semester
                subjects = []
                for i in semesters:
                    subjects_obj = i.subjects.all()
                    for j in subjects_obj:
                        subjects.append(j)
                subjects_count = len(subjects)
                # Count teachers in the branch - from reverse query on branch
                teachers = Teacher.objects.filter(branch=branch_obj)
                teachers_count = teachers.count()
                token['batches'] = batches_count
                token['semesters'] = semesters_count
                token['subjects'] = subjects_count
                token['teachers'] = teachers_count
                token['admin_obj'] = admin_serializer.data        
        return token
    
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
