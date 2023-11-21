from rest_framework import serializers
from .models import Timetable,Schedule,Lecture,Classroom
from Manage.serializers import SubjectSerializer
from StakeHolders.serializers import TeacherProfileSerializer

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['slug','class_name']

class LectureSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    classroom = ClassRoomSerializer() 
    teacher = TeacherProfileSerializer()
    class Meta:
        model = Lecture
        fields = ['slug','teacher','subject','classroom','start_time','end_time']

class ScheduleSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['slug', 'day', 'lectures']

    def get_lectures(self, schedule):        
        lectures = schedule.lectures.all().order_by('start_time')        
        serializer = LectureSerializer(lectures, many=True)
        return serializer.data

class TimetableSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True)
    class Meta:
        model = Timetable
        fields = ['slug','schedules']