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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches(request):     
    try:        
        if request.user.role == 'admin':
            # If batch is not from current year deactivate it
            batch_objects = Batch.objects.all()
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            batches = branch_obj.batches.all()            
            if batches.exists():                            
                batch_serialized_obj = BatchSerializer(batches,many=True)
                data = {'data':batch_serialized_obj.data}
                return JsonResponse(data,status=200)
            else:                
                data = {"data":"Currently there are no active batches"}
                return JsonResponse(data,status=500)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batches(request):
    try:
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)
            if body.get('batch_name') and len(body['batch_name']) > 0:
                if admin_obj.branch.batches.filter(batch_name=body['batch_name']):
                        raise Exception('Batch already exists!')
                start_year, end_year = body['batch_name'].split('-')
                batch_obj = Batch(batch_name=body['batch_name'],start_year=start_year,end_year=end_year)
                batch_obj.save()
                admin_obj.branch.batches.add(batch_obj)            
                batch_serialized_obj = BatchSerializer(batch_obj,many=False)            
                data = {'data':batch_serialized_obj.data}
                return JsonResponse(data,status=200)
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters(request):
    try:
        if request.user.role == 'admin':
            body = request.GET
            admin_obj = Admin.objects.get(profile=request.user)
            if body.get('batch_slug') and len(body['batch_slug']) > 0:
                batch_obj = admin_obj.branch.batches.get(slug=body['batch_slug'])        
                if batch_obj:
                    semesters = batch_obj.semesters
                    if semesters.exists():
                        semesters_serialized = SemesterSerializer(semesters,many=True)
                        data = {'data':semesters_serialized.data}
                        return JsonResponse(data,status=200)
                    else:
                        data = {"data":"Currently there are no active semesters in this batch"}
                        return JsonResponse(data,status=500)               
                else:
                    raise Exception('Batch does not found')
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_semester(request):
    try:
        if request.user.role == 'admin':
            body = request.data            
            if body.get('batch_slug') and len(body['batch_slug']) > 0 and body.get('semester_number') and int(body['semester_number']) > 0 and body.get('start_date') and body.get('end_date'):
                batch_obj = Batch.objects.get(slug = body['batch_slug'])
                if batch_obj:
                    if batch_obj.semesters.filter(no=body['semester_number']):
                        raise Exception('Please add a unique semester')
                    start = datetime.strptime(body.get('start_date'), '%Y-%m-%d').date()
                    end = datetime.strptime(body.get('end_date'), '%Y-%m-%d').date()
                    semester_obj = Semester(no=body['semester_number'],start_date=start,end_date=end)
                    semester_obj.save()
                    batch_obj.semesters.add(semester_obj)
                    semester_serialized_obj = SemesterSerializer(semester_obj,many=False)            
                    data = {'data':semester_serialized_obj.data}
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('batch not found')                    
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects(request):
    try:
        if request.user.role == 'admin':
            body = request.GET            
            if body.get('semester_slug') and len(body['semester_slug']) > 0:
                semester_obj = Semester.objects.get(slug=body.get('semester_slug'))
                if semester_obj:
                    subjects = semester_obj.subjects
                    if subjects.exists():
                        subjects_serialized = SubjectSerializer(subjects,many=True)
                        data = {'data':subjects_serialized.data}
                        return JsonResponse(data,status=200)
                    else:
                        data = {"data":"Currently there are no active subjects in this semester"}
                        return JsonResponse(data,status=500)               
                else:
                    raise Exception('Semester does not found')
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subjects(request):
    try:
        if request.user.role == 'admin':
            body = request.data
            semester_slug = body['semester_slug']
            semester_obj = Semester.objects.get(slug = semester_slug)
            if semester_obj:
                if semester_obj.subjects.filter(code=body.get('subject_code')):
                        raise Exception('Subject is already added to the semester')
                if not body.get('subject_name') or not body.get('subject_code') or not body.get('subject_credit'):
                    raise Exception('Provide all parameters')
                with transaction.atomic():                               
                    subject_obj = Subject(subject_name = body.get('subject_name'),code= body.get('subject_code'),credit=body.get('subject_credit'))
                    subject_obj.save()
                    semester_obj.subjects.add(subject_obj)
                added_subject = SubjectSerializer(subject_obj,many=False)
                data = {'subject':added_subject.data}
                return JsonResponse(data,status=200)
            else:
                raise Exception('Semester does not found')
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:        
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers(request):
    try:
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            teachers = Teacher.objects.filter(branch = branch_obj)            
            if teachers.exists():
                teachers_serialized = TeacherSerializer(teachers,many=True)
                data = {'teachers':teachers_serialized.data}
                return JsonResponse(data,status=200)
            else:
                data = {"data":"Currently there are no active teachers"}
                return JsonResponse(data,status=500)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_teacher(request):
    try:
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            body = request.data
            if 'email' not in body or not body['email']:
                raise serializers.ValidationError("Email is required and cannot be empty.")
            
            if 'password' not in body or not body['password'] or len(body['password']) < 8:
                raise serializers.ValidationError("Password is required and cannot be empty.")
            
            if 'name' not in body or not body['name']:
                raise serializers.ValidationError("Name is required and cannot be empty.")
            
            if 'ph_no' not in body or not body['ph_no']:
                raise serializers.ValidationError("Phone number is required and cannot be empty.")
            # Create an Profile object
            with transaction.atomic():
                user_obj = User(name=body['name'],email=body['email'],ph_no=body['ph_no'],role='teacher',email_verified=True)
                user_obj.set_password(body['password'])
                user_obj.save()
                # Create an teacher object
                teacher_obj = Teacher.objects.create(profile=user_obj,branch=branch_obj)
            teachers_serialized = TeacherSerializer(teacher_obj,many=False)
            data = {'teacher':teachers_serialized.data}
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subjects_to_teacher(request):
    try:
        if request.user.role == 'admin':            
            body = request.data
            if 'teacher_id' not in body or not body['teacher_id']:
                raise serializers.ValidationError("Please pass unique id of the teacher")            
            if 'selected_subjects' not in body:
                raise serializers.ValidationError("Pleae pass a valid subjects array")            
            teacher_obj = Teacher.objects.get(id=body['teacher_id'])                        
            with transaction.atomic():
                if len(body['selected_subjects']) <= 0:
                    teacher_obj.subjects.clear()
                else:
                    for i in body['selected_subjects']:                    
                        subject_obj = Subject.objects.get(slug=i)                    
                        teacher_obj.subjects.add(subject_obj)
            teachers_serialized = TeacherSerializer(teacher_obj,many=False)
            data = {'teacher':teachers_serialized.data}            
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects_of_current_batch(request):
    try:
        if request.user.role == 'admin':
            body = request.GET                        
            if body.get('batch_slug') and len(body['batch_slug']) > 0 and body.get('teacher_id'):
                batch_obj = Batch.objects.get(slug=body.get('batch_slug'))
                teacher_obj = Teacher.objects.get(id=body.get('teacher_id'))
                teachers_subjects = teacher_obj.subjects.all()                
                if batch_obj:
                    semesters = batch_obj.semesters.all()                    
                    subjects = []                    
                    for i in semesters:                        
                        subject_queryset = i.subjects.values()                        
                        if subject_queryset.exists():
                            for i in list(subject_queryset):
                                if teachers_subjects.filter(slug=i['slug']).first():
                                    i['selected'] = True
                                else:
                                    i['selected'] = False
                                subjects.append(i)
                    if(len(subjects) == 0):
                        data = {'data':'No subjects are there...Please add some'}
                        return JsonResponse(data,status=302)                    
                    data = {'data':subjects}
                    return JsonResponse(data,status=200)            
                else:
                    raise Exception('Batch does not found')
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)