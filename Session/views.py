from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SessionSerializer,AttendanceSerializer,SessionSerializerHistory,SurveySerializer
from .models import Session,Attendance,Survey,SurveyOption
from Manage.models import Lecture,GPSCoordinates
from django.utils import timezone
import ipaddress
from StakeHolders.models import Student,Teacher
import os
import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction
from django.core.cache import cache


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
         
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance_for_absent_student(request):
    data = {'data':None,'error':False,'message':None}
    try:    
        if request.user.role == 'teacher':            
            body = request.data
            if 'attendance_slug' in body:
                attendance_obj = Attendance.objects.filter(slug=body['attendance_slug']).first()
                if attendance_obj:
                    if not attendance_obj.is_present:
                        attendance_obj.is_present = True
                        attendance_obj.manual = True
                        attendance_obj.marking_time = datetime.datetime.now()
                        attendance_obj.save()
                        data['data'] = True
                        return Response(data,status=200)
                    else:
                        raise Exception("Attendance has already been marked!!")
                else:                    
                    raise Exception("Attendance object does not exist")
            else:
                raise Exception("Parameters missing")
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)
    
import math

def haversine_distance_in_meters(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters

    # Convert latitude and longitude from degrees to radians
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) * math.sin(d_lat / 2) +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
        math.sin(d_lon / 2) * math.sin(d_lon / 2)
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in meters
    distance = R * c

    return distance

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance_for_student(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            if cache.get(f"attendance_{student_obj.slug}"):
                raise Exception("You've recently tried to mark your attendace....try again after a few seconds!!")
            cache.set(f"attendance_{student_obj.slug}", 'lock', timeout=10)
            if student_obj:
                body = request.data
                if 'lecture_slug' in body and 'latitude' in body and 'longitude' in body:
                    lecture_obj = Lecture.objects.filter(slug=body['lecture_slug']).first()
                    if lecture_obj: 
                        classroom_coords = lecture_obj.classroom.gps_coordinates                        
                        distance_in_meters = haversine_distance_in_meters(float(classroom_coords.latt), float(classroom_coords.long), body['latitude'],body['longitude'])                        
                        print(distance_in_meters)
                        if distance_in_meters > 100:
                            raise Exception("You're out of the predefined boundry of the premises!!")
                        session_obj = Session.objects.filter(lecture=lecture_obj).first()
                        if session_obj:
                            if session_obj.active == 'ongoing':
                                attendance_obj = session_obj.attendances.filter(student=student_obj).first()
                                if attendance_obj:
                                    with transaction.atomic():
                                        if not attendance_obj.is_present:
                                            coordinates_obj = GPSCoordinates.objects.create(title=f"student_{student_obj.slug}",long=body['latitude'],latt=body['longitude'])
                                            attendance_obj.is_present = True                                            
                                            attendance_obj.coordinates = coordinates_obj
                                            attendance_obj.on_premises = True
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
        if request.user.role == 'teacher' or request.user.role == 'admin':
            if session_id:
                session_obj = Session.objects.filter(session_id=session_id).first()
                if session_obj:
                    session_serialized = SessionSerializerHistory(session_obj)
                    data['data'] = session_serialized.data
                    return Response(data,status=200)
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_survey_for_a_lecture(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                body = request.data                
                if 'survey_title' in body and 'type' in body and 'allowd_choices' in body and 'lecture_slug' in body and 'options' in body:
                    lecture_obj = Lecture.objects.filter(slug=body['lecture_slug']).first()
                    if lecture_obj:
                        active_survey = lecture_obj.survey_set.filter(active=True).first()
                        if active_survey:
                            raise Exception('There is already an active survey for the lecture, Please make it inactive to add another survey!!')                        
                        survey_obj = Survey.objects.create(title=body['survey_title'],type=body['type'],allowd_choices=body['allowd_choices'],lecture=lecture_obj)
                        # set the survey options
                        for option in body['options']:
                            option_obj = SurveyOption.objects.create(option=option)
                            survey_obj.options.add(option_obj)
                        # Add the students who are allowed to mark the survey
                        for batch in lecture_obj.batches.all():
                            students = batch.students.all()
                            survey_obj.allowed_students.add(*students)
                        survey_obj.save()
                        survey_serialized = SurveySerializer(survey_obj)
                        data['data'] = survey_serialized.data
                        return Response(data,status=200)
                    else:
                        raise Exception("Lecture does not exist")
                else:
                    raise Exception("Parameters missing")
            else:
                raise Exception('Teacher does not exists')
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_survey(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            if student_obj:
                body = request.data
                if 'survey_slug' in body and 'marked_option_slug' in body:
                    survey_obj = Survey.objects.filter(slug=body['survey_slug']).first()
                    if survey_obj:
                        # Check if student is eligible for marking the survey
                        if survey_obj.allowed_students.contains(student_obj):
                            marked_option_obj = survey_obj.options.filter(slug=body['marked_option_slug']).first()
                            if marked_option_obj:
                                if survey_obj.allowd_choices == 'single':
                                    rest_of_the_options = survey_obj.options.all().exclude(id=marked_option_obj.id)
                                    for option in rest_of_the_options:
                                        if option.student.contains(student_obj):
                                            # option.student.remove(student_obj)
                                            raise Exception("You've already marked your choice!!")  
                                    marked_option_obj.student.add(student_obj)
                                    data['message'] = "You're submission has been successfully marked!!"
                                    return Response(data,status=200)
                            else:
                                raise Exception("Marked option does not exist")
                        else:
                            raise Exception("You're not eligible for marking this survey")
                    else:
                        raise Exception('Survey does not exist')
            else:
                raise Exception('Student does not exist')
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_survey_details(request,lecture_slug):
    data = {'data':None,'error':False,'message':None}    
    try:
        if request.user.role == 'teacher':
            if lecture_slug:
                lecture_obj = Lecture.objects.filter(slug=lecture_slug).first()
                if lecture_obj:                    
                    survey = lecture_obj.survey_set.all()
                    survey_serialized = SurveySerializer(survey,many=True)
                    data['data'] = survey_serialized.data
                    return Response(data,status=200)
                else:
                    raise Exception('Lecture does not exists')
            else:
                raise Exception("Parameters missing")
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True     
        return Response(data,status=500)   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_survey(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                body = request.data                
                if 'survey_slug' in body:
                    survey_obj = Survey.objects.filter(slug=body['survey_slug']).first()
                    if survey_obj:
                        if survey_obj.active == False:
                            raise Exception('Survey is already inactived')    
                        survey_obj.active = False
                        survey_obj.save()
                        data['message'] = "The survey has been inactivated successfully!!"
                        return Response(data,status=200)
                    else:
                        raise Exception('Survey does not exist')
                else:
                    raise Exception("Parameters missing")
            else:
                raise Exception("You're not allowed to perform this action")
        else:
            raise Exception("You're not allowed to perform this action")
    
    except Exception as e:
        print(e)
        data['message'] = str(e)
        data['error'] = True     
        return Response(data,status=500)   