from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SessionSerializer,AttendanceSerializer,SessionSerializerHistory
from .models import Session,Attendance
from Manage.models import Lecture
from django.utils import timezone
import ipaddress
from StakeHolders.models import Student,Teacher
import os
import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lecture_session(request):
    data = {'data':None,'error':False,'message':None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                body = request.data
                if 'lecture_slug' in body:
                    lecture_obj = Lecture.objects.filter(slug=body['lecture_slug']).first()
                    if lecture_obj:
                        batches = lecture_obj.batches.all()                        
                        current_time = datetime.datetime.now().time()
                        if current_time >= lecture_obj.start_time and current_time <= lecture_obj.end_time:
                            lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=datetime.datetime.today().date())
                            if created:           
                                students = Student.objects.filter(batch__in=batches)
                                for student in students:
                                    attendance_obj = Attendance.objects.create(student=student)
                                    lecture_session.attendances.add(attendance_obj)
                                    lecture_session_serialized = SessionSerializer(lecture_session)
                                    data['data'] = lecture_session_serialized.data                        
                            if created:
                                print('newely creted')
                                pass
                            else:
                                if lecture_session.active == 'pre':
                                    lecture_session.active = 'ongoing'
                                    lecture_session.save()
                            lecture_session_serialized = SessionSerializer(lecture_session)
                            data['data'] = lecture_session_serialized.data
                            return Response(data,status=200)
                        else:
                            raise Exception(f'You cannot start the session yet!!')
                    else:
                        raise Exception('Lecture does not exists')
                else:
                    raise Exception('Parameters missing')
            else:
                raise Exception('Teacher does not exists')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:   
        print(e)      
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)

def authenticate_ip(ip,network_part):        
    user_network_addr = '.'.join(ip.split('.')[:network_part])
    if os.environ.get('router_network_addr') == user_network_addr:
        return True
    return False
         
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance_for_student(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':            
            student_obj = Student.objects.filter(profile=request.user).first()
            if student_obj:
                body = request.data
                if 'lecture_slug' in body:
                    lecture_obj = Lecture.objects.filter(slug=body['lecture_slug']).first()
                    if lecture_obj:                                                
                        if ipaddress.IPv4Address(request.META['REMOTE_ADDR']) in ipaddress.IPv4Network(f'{lecture_obj.classroom.router.network_add}/{lecture_obj.classroom.router.CIDR}'):                            
                            session_obj = Session.objects.filter(lecture=lecture_obj).first()
                            if session_obj:
                                if session_obj.active == 'ongoing':
                                    attendance_obj = session_obj.attendances.filter(student=student_obj).first()
                                    if attendance_obj:
                                        if not attendance_obj.is_present:
                                            attendance_obj.is_present = True
                                            attendance_obj.marking_ip = request.META['REMOTE_ADDR']
                                            attendance_obj.marking_time = datetime.datetime.now()
                                            attendance_obj.save()
                                            channel_name = session_obj.session_id
                                            attendance_serialized = AttendanceSerializer(attendance_obj)
                                            async_to_sync(channel_layer.group_send)(channel_name, {"type": "attendance.marked",'message':attendance_serialized.data})
                                            data['data'] = True
                                            data['code'] = 100
                                            return Response(data,status=200)
                                        else:
                                            data['code'] = 100                                                                            
                                            raise Exception("Your attendance has already been marked")
                                    else:
                                            raise Exception("You're not part of this attendance session :\\")
                                elif session_obj.active == 'post':
                                    data['code'] = 100
                                    raise Exception('Attendance session has been ended!!')
                                else:
                                    raise Exception('Attendance session has not been started yet!!')
                            else:
                                raise Exception('Session does not exist')
                        else:
                            raise Exception(f'Please connect to {lecture_obj.classroom.router.hostname}...then try again!!')
                    else:
                        raise Exception('Lecture does not exists')
                else:
                    raise Exception('Parameters missing')
            else:
                raise Exception('Student does not exists')            
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_data_for_export(request,session_id):
    data = {'data':None,'error':False,'message':None}
    body = request.query_params
    try:
        if request.user.role == 'teacher':
            if session_id:
                session_obj = Session.objects.filter(session_id=session_id).first()
                if session_obj:
                    session_serialized = SessionSerializerHistory(session_obj)
                    data['data'] = session_serialized.data
                    return Response(data,status=290)
                else:
                    raise Exception('Session does not exists')
            else:
                raise Exception("Parameters missing")
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True     
        return Response(data,status=500)   