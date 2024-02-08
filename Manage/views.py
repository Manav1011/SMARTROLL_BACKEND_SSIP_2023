from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from Manage.models import Division, Semester,Batch,TimeTable,Schedule,Classroom,Lecture
from StakeHolders.models import Admin,Teacher
from Profile.models import Profile
from .serializers import SemesterSerializer,DivisionSerializer,BatchSerializer,SubjectSerializer,TimeTableSerializer,ClassRoomSerializer
from Manage.models import Semester,Branch,Subject
from django.contrib.auth import get_user_model
from StakeHolders.serializers import TeacherSerializer
import datetime
# Create your views here.

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_object_counts(request):
    try:        
        if request.user.role == 'admin':
            data = {'semesters':0,'divisons':0,'batches':0}
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            branch = admin_obj.branch_set.first()
            semesters = branch.semester_set.all()
            semester_count = len(semesters)
            divisions = []
            for i in semesters:
                sem_divs = i.division_set.all()
                divisions.extend(sem_divs)
            division_count = len(divisions)
            batches = []
            for i in divisions:
                div_batches = i.batch_set.all()
                batches.extend(div_batches)
            batch_count = len(batches)            
            data['semesters'] = semester_count
            data['divisons'] = division_count
            data['batches'] = batch_count
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_semester(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':  
            body = request.data
            if 'no' in body and 'start_year' in body and 'end_year' in body:
                admin_obj = Admin.objects.get(profile=request.user)
                # We'll have to get the counts of semester, divisions, batches
                branch_obj = admin_obj.branch_set.first()
                if branch_obj:
                    semester_obj,created = Semester.objects.get_or_create(no=body['no'],branch=branch_obj)
                    if created:
                        semester_obj.start_year =body['start_year']
                        semester_obj.end_year = body['end_year']
                        semester_obj.save()
                        semester_serialized = SemesterSerializer(semester_obj)
                        data['data'] = semester_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Semester already added')
                else:
                    raise Exception('No branch found')
            else:
                raise Exception('Provide all the parameters')                        
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data,status=500)    
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':              
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            branch_obj = admin_obj.branch_set.first()
            semesters = branch_obj.semester_set.all().filter(status=True)
            if semesters.exists():
                semesters_serialized = SemesterSerializer(semesters,many=True)
                data['data'] = semesters_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('Semester Does Not Exists')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['error'] = True
        data['message'] = str(e)    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_division(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            if 'division_name' in body and 'semester_slug' in body :
                semester_obj = Semester.objects.filter(slug=body['semester_slug']).first()                
                if semester_obj and semester_obj.branch.admins.contains(admin_obj):
                    division_obj,created = Division.objects.get_or_create(division_name = body['division_name'],semester=semester_obj)
                    if created:
                        division_serialized = DivisionSerializer(division_obj)
                        timetable_obj = TimeTable.objects.create(division=division_obj)
                        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
                        for day in days:
                            Schedule.objects.create(day=day, timetable=timetable_obj)
                        data['data'] = division_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('division already added')
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Credentials not provided")
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batch(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            if 'batch_name' in body and 'division_slug' in body :
                division_obj = Division.objects.filter(slug=body['division_slug']).first()                
                if division_obj and division_obj.semester.branch.admins.contains(admin_obj):
                    batch_obj,created = Batch.objects.get_or_create(batch_name = body['batch_name'],division=division_obj)
                    if created:
                        batch_serialized = BatchSerializer(batch_obj)
                        data['data'] = batch_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('division already added')
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Credentials not provided")
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.query_params
            admin_obj = Admin.objects.get(profile=request.user)
            if 'division_slug' in body :
                division_obj = Division.objects.filter(slug=body['division_slug']).first()
                if division_obj and division_obj.semester.branch.admins.contains(admin_obj):
                   batches = division_obj.batch_set.all()
                   batches_serialized = BatchSerializer(batches,many=True)
                   data['data'] = batches_serialized.data
                   return JsonResponse(data,status=200)
                else:
                   raise Exception('Divison does not exist')
            else:
                raise Exception("Credentials not provided")
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_divisions(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.query_params
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            if 'semester_slug' in body:
                semester_obj = Semester.objects.filter(slug=body.get('semester_slug')).first()
                if semester_obj and semester_obj.branch.admins.contains(admin_obj):
                    divisions = semester_obj.division_set.all()
                    division_serialized = DivisionSerializer(divisions, many=True)
                    data['data'] = division_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Choose the correct semester to get the divisions")            
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subject(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':  
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)       
            if 'code' in body and 'subject_name' in body and 'credit' in body and 'semester_slug' in body:
                semester_obj = Semester.objects.filter(slug= body['semester_slug']).first()
                if semester_obj and semester_obj.branch.admins.contains(admin_obj):
                    subject_obj,created = Subject.objects.get_or_create(code=body['code'],subject_name = body['subject_name'], credit = body['credit'],semester = semester_obj)
                    if created:
                        subject_serialized = SubjectSerializer(subject_obj)
                        data['data'] = subject_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception("Subject is already exist")
                else:
                    raise Exception("Semester does not exist")
            else:
                raise Exception("Provide the proper credentials")        
        else:
            raise Exception("You're not allowed to perform this action")            

    except Exception as e:
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':            
            admin_obj = Admin.objects.get(profile=request.user)                                    
            branch_obj = admin_obj.branch_set.first()            
            subjects = Subject.objects.filter(semester__branch=branch_obj)
            subject_serialized = SubjectSerializer(subjects, many=True)
            data['data'] = subject_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True
        return JsonResponse(data,status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_teacher(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            branch_obj = admin_obj.branch_set.first()
            if 'name' in body and 'email' in body and 'ph_no' in body:
                profile_obj,created = Profile.objects.get_or_create(name=body['name'],email=body['email'],ph_no=body['ph_no'],role='teacher')
                if created:
                    teacher_obj = Teacher.objects.create(profile=profile_obj)
                    branch_obj.teachers.add(teacher_obj)
                    teacher_serialized = TeacherSerializer(teacher_obj)
                    data['data'] = teacher_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Teacher already exists')
            else:
                raise Exception('Credentials not provided')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':            
            admin_obj = Admin.objects.get(profile=request.user)            
            branch_obj = admin_obj.branch_set.first()
            teachers = branch_obj.teachers.all()
            teacher_serialized = TeacherSerializer(teachers,many=True)
            data['data'] = teacher_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':            
            body = request.query_params
            if 'division_slug' in body:
                division_obj = Division.objects.filter(slug=body['division_slug']).first()
                timetable_obj = TimeTable.objects.get(division=division_obj)
                timetable_serialized = TimeTableSerializer(timetable_obj)
                data['data'] = timetable_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('Credentials not provided')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_configs(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch_set.first()
            teachers = branch_obj.teachers.all()
            classrooms = branch_obj.classroom_set.all()
            batches = Batch.objects.filter(division__semester__branch=branch_obj)
            subjects = Subject.objects.filter(semester__branch=branch_obj)
            teachers_serialized = TeacherSerializer(teachers,many=True)
            classrooms_serialized = ClassRoomSerializer(classrooms,many=True)
            batches_serialized = BatchSerializer(batches,many=True)        
            subjects_serialized = SubjectSerializer(subjects,many=True)
            data['data'] = {}
            data['data']['teachers'] = teachers_serialized.data
            data['data']['classrooms'] = classrooms_serialized.data
            data['data']['batches'] = batches_serialized.data
            data['data']['subjects'] = subjects_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lecture_to_schedule(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            body = request.data
            if "schedule_slug" in body and "start_time" in body and "end_time" in body and "type" in body and "subject_slug" in body and "teacher" in body and "classroom" in body and "batches" in body and "schedule" in body:
                start_time  = datetime.strptime(body['start_time'], "%H:%M").time()
                end_time  = datetime.strptime(body['end_time'], "%H:%M").time()
                subject = Subject.objects.get(slug=body['subject_slug'])
                teacher = Teacher.objects.get(slug=body['teacher_slug'])
                classroom = Classroom.objects.get(slug=body['classroom_slug'])
                schedule = Schedule.objects.get(slug=body['schedule_slug'])
                lecture_obj = Lecture(start_time=start_time,end_time=end_time,type=body['type'],subject=subject,teacher=teacher,classroom=classroom,schedule=schedule)
            else:
                raise Exception('Credentials Missing')   
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)