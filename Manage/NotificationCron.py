from .models import Lecture,Schedule
from pywebpush import webpush, WebPushException
import json
from django.conf import settings
import threading
from datetime import datetime

def send_notification_async(time):
    current_datetime = datetime.now()
    current_day_name = current_datetime.strftime('%A')
    schedules = Schedule.objects.filter(day=current_day_name.lower())
    for day in schedules:
        lectures = Lecture.objects.filter(schedule=day,start_time=time) 
        for lecture in lectures:
            if lecture.teacher.web_push_subscription:
                subscriptions = lecture.teacher.web_push_subscription.all()
                for subscription in subscriptions:
                    try:
                        notification_body=f"You have a session scheduled at {lecture.start_time} for {lecture.subject.subject_name} | Semester - {lecture.subject.semester.no} at {lecture.classroom.class_name}"                        
                        webpush(subscription_info=json.loads(subscription.subscription),data=notification_body,vapid_private_key=settings.VAPID_PRIVATE_KEY,vapid_claims=settings.VAPID_CLAIMS)
                    except WebPushException as e:
                        print(e)

# def NotifyTeachers9_15():
#     # send_notification_async("22:00:00")
#     thread = threading.Thread(target=send_notification_async,kwargs={"time":"0:15:00"})
#     thread.start()

def NotifyTeachers10_30():    
    thread = threading.Thread(target=send_notification_async,kwargs={"time":"10:30:00"})
    thread.start()

def NotifyTeachers11_30():    
    thread = threading.Thread(target=send_notification_async,kwargs={"time":"11:30:00"})
    thread.start()

def NotifyTeachers13_00():    
    thread = threading.Thread(target=send_notification_async,kwargs={"time":"13:00:00"})
    thread.start()

def NotifyTeachers14_00():    
    thread = threading.Thread(target=send_notification_async,kwargs={"time":"14:00:00"})
    thread.start()

def NotifyTeachers15_15():    
    thread = threading.Thread(target=send_notification_async,kwargs={"time":"15:15:00"})
    thread.start()

def NotifyTeachers16_15():
    thread = threading.Thread(target=send_notification_async,kwargs={"time":"16:15:00"})
    thread.start()
