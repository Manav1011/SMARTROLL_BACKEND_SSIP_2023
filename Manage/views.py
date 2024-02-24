from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from Manage.models import Division, Semester,Batch,TimeTable,Schedule,Classroom,Lecture,Term,Link
from StakeHolders.models import Admin,Teacher,Student
from Profile.models import Profile
from .serializers import SemesterSerializer,DivisionSerializer,BatchSerializer,SubjectSerializer,TimeTableSerializer,ClassRoomSerializer,LectureSerializer,TermSerializer,TimeTableSerializerForTeacher,TimeTableSerializerForStudent,LectureSerializerForHistory
from Manage.models import Semester,Subject
from Session.models import Session,Attendance
import pandas as pd
from django.contrib.auth import get_user_model
from StakeHolders.serializers import TeacherSerializer
import datetime
from django.conf import settings as django_settings
from django.core.mail import send_mail
from threading import Thread
# Create your views here.

User = get_user_model()

def send_activation_email(receiver,teacher_slug):    
    sender_email = django_settings.EMAIL_HOST_USER
    sent = False
    url = f'https://ea5b-2405-201-2024-b862-a240-d7c6-e920-c012.ngrok-free.app/teacher_activation/{teacher_slug}'
    try:
        send_mail('Activate Your Acount',url, from_email=sender_email,recipient_list=[receiver])
        sent=True
    except Exception as e:             
        sent = False
    return sent


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_object_counts(request):
    try:        
        if request.user.role == 'admin':
            data = {'terms':0,'semesters':0,'divisons':0,'batches':0}
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            branch = admin_obj.branch_set.first()
            terms = branch.term_set.all()
            term_count = len(terms)
            semesters = []
            for i in terms:
                term_sems = i.semester_set.all()
                semesters.extend(term_sems)
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
            data['terms'] = term_count
            data['semesters'] = semester_count
            data['divisons'] = division_count
            data['batches'] = batch_count
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data = {"data":str(e)}
        return JsonResponse(data,status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_term(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':  
            body = request.data
            if 'start_year' in body and 'end_year' in body:
                admin_obj = Admin.objects.get(profile=request.user)
                # We'll have to get the counts of semester, divisions, batches
                branch_obj = admin_obj.branch_set.first()
                if branch_obj:
                    term_obj,created = Term.objects.get_or_create(start_year=body['start_year'],end_year=body['end_year'],branch=branch_obj)
                    if created:
                        term_obj.start_year =body['start_year']
                        term_obj.end_year = body['end_year']
                        term_obj.save()
                        term_serialized = TermSerializer(term_obj)
                        data['data'] = term_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Term already added')
                else:
                    raise Exception('No branch found')
            else:
                raise Exception('Provide all the parameters')                        
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data,status=500) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_terms(request):    
    try:        
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'admin':              
            admin_obj = Admin.objects.get(profile=request.user)
            # We'll have to get the counts of semester, divisions, batches
            branch_obj = admin_obj.branch_set.first()
            terms = branch_obj.term_set.all()
            if terms.exists():
                terms_serialized = TermSerializer(terms,many=True)
                data['data'] = terms_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('No Term Added')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)   
        return JsonResponse(data,status=500)   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_semester(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            if 'no' in body and 'term_slug' in body:
                admin_obj = Admin.objects.get(profile=request.user)
                # We'll have to get the counts of semester, divisions, batches
                term_obj = Term.objects.filter(slug=body['term_slug']).first()
                if term_obj:
                    semester_obj,created = Semester.objects.get_or_create(no=body['no'],term=term_obj)
                    if created:                                                
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
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return JsonResponse(data,status=500)    
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters(request):
    try:        
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            if 'term_slug' in body:
                # We'll have to get the counts of semester, divisions, batches
                term_obj = Term.objects.filter(slug=body['term_slug']).first()
                if term_obj:
                    semesters = term_obj.semester_set.all().filter(status=True)
                    if semesters.exists():
                        semesters_serialized = SemesterSerializer(semesters,many=True)
                        data['data'] = semesters_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Semester Does Not Exists')
                else:
                        raise Exception('Term Does Not Exists')
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)   
        return JsonResponse(data,status=500) 
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_division(request):
    try:    
        data = {'data':None,'error':False,'message':None}    
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)            
            if 'division_name' in body and 'semester_slug' in body and len(body['division_name']) > 0:
                semester_obj = Semester.objects.filter(slug=body['semester_slug']).first()                
                if semester_obj and semester_obj.term.branch.admins.contains(admin_obj):
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
        print(e)
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
            if 'batch_name' in body and 'division_slug' in body and len(body['batch_name']) > 0:
                division_obj = Division.objects.filter(slug=body['division_slug']).first()                
                if division_obj and division_obj.semester.term.branch.admins.contains(admin_obj):
                    batch_obj,created = Batch.objects.get_or_create(batch_name = body['batch_name'],division=division_obj)
                    if created:
                        batch_serialized = BatchSerializer(batch_obj)
                        data['data'] = batch_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Batch already added')
                else:
                    raise Exception("This Semester does not exist")
            else:
                raise Exception("Credentials not provided")
            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
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
                if division_obj and division_obj.semester.term.branch.admins.contains(admin_obj):
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
        print(e)
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
                if semester_obj and semester_obj.term.branch.admins.contains(admin_obj):
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
        print(e)
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
                if semester_obj and semester_obj.term.branch.admins.contains(admin_obj):
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
        print(e)
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
            subjects = Subject.objects.filter(semester__term__branch=branch_obj)
            subject_serialized = SubjectSerializer(subjects, many=True)
            data['data'] = subject_serialized.data
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:        
        print(e)
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
            if 'name' in body and 'email' in body:
                profile_obj,created = Profile.objects.get_or_create(name=body['name'],email=body['email'],role='teacher')
                if created:
                    teacher_obj = Teacher.objects.create(profile=profile_obj)
                    branch_obj.teachers.add(teacher_obj)
                    teacher_serialized = TeacherSerializer(teacher_obj)
                    Thread(target=send_activation_email,args=(body['email'],teacher_obj.slug)).start()
                    data['data'] = teacher_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Teacher is already added, Please check the mail!!')
            else:
                raise Exception('Credentials not provided')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
def activate_teacher_acount(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.data
        if 'password' in body and 'teacher_slug' in body:
            teacher_obj = Teacher.objects.filter(slug=body['teacher_slug']).first()
            if teacher_obj:                
                if not teacher_obj.profile.is_active:
                    teacher_obj.profile.is_active = True
                    teacher_obj.profile.set_password(body['password'])
                    teacher_obj.profile.save()
                    data['data'] = True
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Teacher is already added')
            else:
                raise Exception('Teacher does not exists')
        else:
            raise Exception('Parameters missing')
    except Exception as e:
        print(e)
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
        print(e)
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
                timetable_obj = TimeTable.objects.filter(division=division_obj).first()
                if timetable_obj:
                    timetable_serialized = TimeTableSerializer(timetable_obj)
                    data['data'] = timetable_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('No timetable exists for this division')
            else:
                raise Exception('Credentials not provided')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_configs(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.query_params
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch_set.first()
            if 'schedule_slug' in body:
                schedule_obj = Schedule.objects.filter(slug=body['schedule_slug']).first()
                division_obj = Division.objects.filter(timetable__schedule = schedule_obj).first()
                semester_obj = division_obj.semester
                if division_obj and semester_obj and schedule_obj: 
                    teachers = branch_obj.teachers.all()
                    classrooms = branch_obj.classroom_set.all()
                    batches = Batch.objects.filter(division=division_obj)
                    subjects = Subject.objects.filter(semester = semester_obj)
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
                    raise Exception('Object Not Found')
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lecture_to_schedule(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            if "schedule_slug" in body and "start_time" in body and "end_time" in body and "type" in body and "subject" in body and "teacher" in body and "classroom" in body and "batches" in body:
                schedule = Schedule.objects.get(slug=body['schedule_slug'])
                start_time  = datetime.datetime.strptime(body['start_time'], "%H:%M").time()
                end_time  = datetime.datetime.strptime(body['end_time'], "%H:%M").time()
                subject = Subject.objects.get(slug=body['subject'])
                teacher = Teacher.objects.get(slug=body['teacher'])
                classroom = Classroom.objects.get(slug=body['classroom'])
                lecture_obj,created = Lecture.objects.get_or_create(start_time=start_time,end_time=end_time,schedule=schedule)
                if created:
                    lecture_obj.type=body['type']
                    lecture_obj.subject=subject
                    lecture_obj.teacher=teacher
                    lecture_obj.classroom=classroom
                    lecture_obj.save()
                    batches = Batch.objects.filter(slug__in=body['batches'])
                    lecture_obj.batches.add(*batches)
                    # Need to create lecture sessions for this particular lecture till the next sunday...after that the cronjob will take care of it
                    today = datetime.datetime.now().date()                    
                    if lecture_obj:
                            batches = lecture_obj.batches.all()
                            lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=today,active='pre')
                            if created:             
                                students = Student.objects.filter(batch__in=batches)
                                for student in students:
                                    attendance_obj = Attendance.objects.create(student=student)
                                    lecture_session.attendances.add(attendance_obj)
                    else:
                        raise Exception('Lecture does not exists')
                    lecture_obj_serialized = LectureSerializer(lecture_obj)
                    data['data'] = lecture_obj_serialized.data
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Lecture already exists for this timeslot')
            else:
                raise Exception('Credentials Missing')               
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_lecture_as_proxy(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            if "prev_lecture_slug" in body and "schedule_slug" in body and "start_time" in body and "end_time" in body and "type" in body and "subject" in body and "teacher" in body and "classroom" in body and "batches" in body:
                prev_lecture_obj = Lecture.objects.filter(slug=body['prev_lecture_slug']).first()
                print(prev_lecture_obj)
                if prev_lecture_obj:
                    schedule = Schedule.objects.get(slug=body['schedule_slug'])
                    start_time  = datetime.datetime.strptime(body['start_time'], "%H:%M").time()
                    end_time  = datetime.datetime.strptime(body['end_time'], "%H:%M").time()
                    subject = Subject.objects.get(slug=body['subject'])
                    teacher = Teacher.objects.get(slug=body['teacher'])
                    classroom = Classroom.objects.get(slug=body['classroom'])
                    lecture_obj,created = Lecture.objects.get_or_create(start_time=start_time,end_time=end_time,schedule=schedule,is_proxy = True)
                    if created:
                        # Create link object 
                        link_obj,created = Link.objects.get_or_create(from_lecture=prev_lecture_obj,to_lecture=lecture_obj)
                        lecture_obj.type=body['type']
                        lecture_obj.subject=subject
                        lecture_obj.teacher=teacher
                        lecture_obj.classroom=classroom
                        lecture_obj.save()
                        batches = Batch.objects.filter(slug__in=body['batches'])
                        lecture_obj.batches.add(*batches)
                        # Need to create lecture sessions for this particular lecture till the next sunday...after that the cronjob will take care of it
                        today = datetime.datetime.now().date()                    
                        if lecture_obj:
                                batches = lecture_obj.batches.all()
                                lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=today,active='pre')
                                if created:           
                                    students = Student.objects.filter(batch__in=batches)
                                    for student in students:
                                        attendance_obj = Attendance.objects.create(student=student)
                                        lecture_session.attendances.add(attendance_obj)
                        else:
                            raise Exception('Lecture does not exists')
                        lecture_obj_serialized = LectureSerializer(lecture_obj)
                        data['data'] = lecture_obj_serialized.data
                        return JsonResponse(data,status=200)
                    else:
                        raise Exception('Lecture already exists for this timeslot')
                else:
                    raise Exception('Lecture does not exists')
            else:
                raise Exception('Credentials Missing')               
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_students_data(request):
    try:
        data = {'data':{'logs':{},'register_count':0,'error_count':0},'error':False,'message':None}
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch_set.first()                 
            if 'sheet_name' in body and 'division_slug' in body and 'students.xlsc' in body:
                divison_obj = Division.objects.filter(slug=body['division_slug']).first()
                if divison_obj:
                    df = pd.read_excel(body['students.xlsc'],sheet_name=body['sheet_name'])
                    df = df.drop(index=range(3))
                    current_batch = None                         
                    for index,row in df.iterrows():    
                        try:
                            if not pd.isna(row[0]):
                                serial_no = row[0]
                                batch = row[1] if not pd.isna(row[1]) else current_batch
                                current_batch = batch
                                enrollment = row[2]
                                name = row[3]
                                gender = row[4]                                
                                batch_obj = divison_obj.batch_set.filter(batch_name=batch).first()
                                if batch_obj:
                                    profile_obj,created = Profile.objects.get_or_create_by_name(name=name,gender=gender,role='student')
                                    if created:                            
                                        student_obj,student_created = Student.objects.get_or_create(profile=profile_obj,sr_no=serial_no,enrollment=enrollment)
                                        if student_created:
                                            batch_obj.students.add(student_obj)
                                            branch_obj.students.add(student_obj)
                                            data['data']['register_count'] += 1
                                            data['data']['logs'][serial_no] = f"Student Created - {serial_no} - {batch[1:]} - {enrollment} - {name} - {gender}"
                                        else:
                                            raise Exception('Student already exists')
                                    else:
                                        raise Exception('Student already exists')
                                else:
                                    raise Exception(f"Batch/Division does not exist for {serial_no} - {batch[1:]} - {enrollment} - {name} - {gender}")                        
                        except Exception as e:
                            print(e)
                            data['data']['error_count'] += 1
                            data['data']['logs'][row[0]] = f"{str(e)} - {serial_no} - {batch[1:]} - {enrollment} - {name} - {gender}"
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('Division not found')
            else:
                raise Exception('Parameters missing')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable_for_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                semesters = teacher_obj.branch_set.first().term_set.filter(status=True).first().semester_set.filter(status=True)
                divisions = Division.objects.filter(semester__in=semesters)
                timetables = TimeTable.objects.filter(division__in=divisions)
                timetable_serialized = TimeTableSerializerForTeacher(instance=timetables,teacher=teacher_obj,many=True)
                data['data'] = timetable_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception('Teacher does not exist')
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable_for_student(request):
    try:
        data = {'data':{'logs':{},'register_count':0,'error_count':0},'error':False,'message':None}
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            if student_obj:
                batches = Batch.objects.filter(students=student_obj)
                division = Division.objects.filter(batch__students=student_obj).first()
                timetables = TimeTable.objects.filter(division=division)    
                timetable_serialized = TimeTableSerializerForStudent(instance=timetables,student=student_obj,batches=batches,many=True)
                data['data'] = timetable_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Student does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects_of_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                lectures = Lecture.objects.filter(teacher=teacher_obj)
                subjects = list({lecture.subject for lecture in lectures})
                subjects_serialized = SubjectSerializer(subjects,many=True)
                data['data'] = subjects_serialized.data
                return JsonResponse(data,status=200)
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecture_sessions_for_teacher(request):
    try:
        data = {'data':None,'error':False,'message':None}
        body = request.query_params
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                if 'subject_slug' in body:
                        subject_obj = Subject.objects.filter(slug=body['subject_slug']).first()
                        if subject_obj:
                            lectures = subject_obj.lecture_set.filter(teacher=teacher_obj,session__active='post')
                            lectures_serialized = LectureSerializerForHistory(lectures,many=True)
                            data['data'] = lectures_serialized.data
                            return JsonResponse(data,status=200)                            
                        else:
                            raise Exception('Subject does not exists')
                else:
                    raise Exception('Parameters Missing')
            else:
                raise Exception("Teacher does not exist")
        else:
            raise Exception("You're not allowed to perform this action")

    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True        
        return JsonResponse(data,status=500)