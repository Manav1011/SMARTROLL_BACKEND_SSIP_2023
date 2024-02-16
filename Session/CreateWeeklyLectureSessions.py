# Script to be ran every sunday
from .models import Session,Attendance
from  Manage.models import Lecture,TimeTable
from datetime import datetime, timedelta
from StakeHolders.models import Student

def return_day_index(day):
    day_mapping = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6        
    }
    return day_mapping[day]

def create_weekly_sessions():
    today= datetime.now().date() - timedelta(days =5)
    timetables = TimeTable.objects.all()
    for timetable in timetables:
        schedules = timetable.schedule_set.all()
        for schedule in schedules:            
            date_for_schedule = today + timedelta(days=return_day_index(schedule.day))
            lectures = schedule.lecture_set.all()
            # Create sessions in each lecture
            for lecture_obj in lectures:
                try:
                    if lecture_obj:
                            batches = lecture_obj.batches.all()
                            lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,day=date_for_schedule,active='pre')
                            if created:                            
                                students = Student.objects.filter(batch__in=batches)
                                for student in students:
                                    attendance_obj = Attendance.objects.create(student=student)
                                    lecture_session.attendances.add(attendance_obj)                                
                            else:
                                pass                        
                    else:
                        raise Exception('Lecture does not exists')
                except Exception as e:
                    print(e)