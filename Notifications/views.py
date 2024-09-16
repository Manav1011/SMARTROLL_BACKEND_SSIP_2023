from django.shortcuts import render
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from pywebpush import webpush, WebPushException
from .serializers import EventSerializer
from rest_framework.response import Response
from .models import Event,Result
from rest_framework.parsers import MultiPartParser, FormParser
from Manage.models import Branch,Subject
from django.conf import settings
from StakeHolders.models import Teacher,Student,NotificationSubscriptions
import pandas as pd
import json

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_event(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'superadmin':            
            body = request.data
            if 'title' in body and 'description' in body and 'branches' in body:
                event_obj = Event.objects.create(title=body['title'],description=body['description'])                
                branches = Branch.objects.filter(slug__in=body['branches'])
                event_obj.branches.add(*branches)
                event_obj_serialized = EventSerializer(event_obj)
                data['data'] = event_obj_serialized.data
                return Response(data,status=200)
            else:
                raise Exception("Parameters missing!!")    
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'superadmin':            
            events = Event.objects.all().order_by('-created_at')
            events_serialized = EventSerializer(events,many=True)
            data['data'] = events_serialized.data            
            return Response(data,status=200)                            
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def end_event(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'superadmin':            
            body = request.data
            if 'event_slug' in body:
                event_obj = Event.objects.filter(slug=body['event_slug']).first()
                if event_obj:
                    if event_obj.status == False:
                        raise Exception('Event already ended')
                    event_obj.status = False
                    event_obj.save()
                    data['message'] = "Event ended successfully!!"
                    return Response(data,status=200)
                else:
                    raise Exception("Event does not exists")
            else:
                raise Exception("Parameters missing!!")    
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_results(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':            
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:                
                if 'subject_slug' in request.data and 'result_csv' in request.data and 'remarks' in request.data and 'total_marks' in request.data:
                    subject_obj = Subject.objects.filter(slug=request.data['subject_slug']).first()
                    if subject_obj:
                        csv_obj = request.data.get('result_csv')
                        df = pd.read_csv(csv_obj)
                        result_add_count = 0
                        for index, row in df.iterrows():                            
                            student_obj = Student.objects.filter(enrollment=row[1]).first()
                            if student_obj:
                                # Check if student studies this subject or not
                                if subject_obj.included_batches.filter(students=student_obj).exists():
                                    # Now we can create a result object
                                    Result.objects.create(total_marks=request.data['total_marks'],gained_marks=row[3],subject=subject_obj,student=student_obj,remarks=request.data['remarks'])
                                    result_add_count+=1
                        data['message'] = f'Result Added Successfully to {result_add_count} students'
                        return Response(data,status=200)
                    else:
                        raise Exception("Subject does not exists")
                else:
                    raise Exception("Parameters Missing!!")    
            else:
                raise Exception("Teacher does not exists!!")
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)
    
@api_view(['POST'])
def notify_users_about_emergency(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        body = request.data
        if 'event' not in body or 'cause' not in body or 'location' not in body:
            raise Exception("Parameters Missing!!")
        
        # Get the user's subscriptions who have subscribed for the alerts
        subscriptions = NotificationSubscriptions.objects.filter(subscription_type='alerts')
        for subscription in subscriptions:
            print(subscription)
            notification_body = f"🚨 EMERGENCY ALERT! 🚨\n {body['cause'].upper()} has been detected at {body['location']}! Please take immediate action and ensure your safety."
            try:
                webpush(subscription_info=json.loads(subscription.subscription),data=notification_body,vapid_private_key=settings.VAPID_PRIVATE_KEY,vapid_claims=settings.VAPID_CLAIMS)
            except WebPushException as e:
                print(e)
        return Response(data,status=200)
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)
