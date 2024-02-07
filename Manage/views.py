from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from StakeHolders.models import Admin,Teacher
from .serializers import BatchSerializer,SemesterSerializer,SubjectSerializer
from StakeHolders.serializers import TeacherSerializer
from Manage.models import Batch,Semester,Subject
from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_object_counts(request):
    try:        
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
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
            data = {'branch':branch_obj.branch_name,'batches':batches_count,'teachers':teachers_count,'semesters':semesters_count,'subjects':subjects_count}
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)