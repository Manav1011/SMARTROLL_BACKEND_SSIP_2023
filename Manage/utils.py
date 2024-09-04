from Manage.models import Lecture,Schedule
from pywebpush import webpush, WebPushException
import json
from django.conf import settings
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