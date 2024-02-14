from .models import Batch, Division,Semester,Subject,Branch,College,TimeTable,Schedule,Lecture,Classroom,Term
from datetime import datetime
from rest_framework import serializers
from Session.models import Session

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_name','slug']

class BranchSerializer(serializers.ModelSerializer):
    college = CollegeSerializer()
    class Meta:
        model = Branch
        fields = ['branch_name','branch_code','slug','college']


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['division_name','slug']


class BatchSerializer(serializers.ModelSerializer):
    division = DivisionSerializer()
    class Meta:
        model = Batch
        fields = ['slug','batch_name','division']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['slug', 'subject_name', 'code', 'credit']
        
class SemesterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Semester
        fields = ['slug','no','status']

class DivisionSerializerForTeacher(serializers.ModelSerializer):
    semester = SemesterSerializer()
    class Meta:
        model = Division
        fields = ['division_name','slug','semester']

class TermSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Term
        fields = ['slug','start_year','end_year']

class SemesterSerializerStudentCred(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Semester
        fields = ['slug','no','status','start_date','end_date','subjects','time_table']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['class_name','slug']

class ScheduleSerializerForTeacher(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['day','slug','lectures']
    
    def __init__(self, teacher=None, *args, **kwargs):
        super(ScheduleSerializerForTeacher, self).__init__(*args, **kwargs)
        self.teacher = teacher
    
    def get_lectures(self,obj):
        lectures = obj.lecture_set.filter(teacher=self.teacher)
        lectures_serialized = LectureSerializer(lectures,many=True)
        return lectures_serialized.data
    
class ScheduleSerializerForStudent(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['day','slug','lectures']
    
    def __init__(self, batches=None, *args, **kwargs):
        super(ScheduleSerializerForStudent, self).__init__(*args, **kwargs)
        self.batches = batches
    
    def get_lectures(self,obj):        
        lectures = obj.lecture_set.filter(batches__in=self.batches)
        lectures_serialized = LectureSerializer(lectures,many=True)
        return lectures_serialized.data        


class TimeTableSerializerForStudent(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()
    division = DivisionSerializerForTeacher()

    class Meta:
        model = TimeTable
        fields = ['slug','division','schedules']
    
    def __init__(self, batches, *args, **kwargs):
        super(TimeTableSerializerForStudent, self).__init__(*args, **kwargs)
        self.batches = batches

    def get_schedules(self,obj):
        current_datetime = datetime.now()
        current_day_name = current_datetime.strftime('%A')
        schedules = obj.schedule_set.filter(day=current_day_name.lower())
        # schedules = obj.schedule_set.filter(day='saturday')
        schedules_serialized = ScheduleSerializerForStudent(instance=schedules,many=True,batches=self.batches)
        return schedules_serialized.data    
    
class TimeTableSerializerForTeacher(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()
    division = DivisionSerializerForTeacher()

    class Meta:
        model = TimeTable
        fields = ['slug','division','schedules']
    
    def __init__(self, teacher, *args, **kwargs):
        super(TimeTableSerializerForTeacher, self).__init__(*args, **kwargs)
        self.teacher = teacher

    def get_schedules(self,obj):
        current_datetime = datetime.now()
        current_day_name = current_datetime.strftime('%A')
        schedules = obj.schedule_set.filter(day=current_day_name.lower())
        # schedules = obj.schedule_set.filter(day='saturday')
        schedules_serialized = ScheduleSerializerForTeacher(instance=schedules,many=True,teacher=self.teacher)
        return schedules_serialized.data    
    
class SessionSerializerForLecture(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id','active','day','created_at']

class LectureSerializerForHistory(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()
    classroom = serializers.SerializerMethodField()
    class Meta:
        model = Lecture
        fields = ['type','classroom','slug','session']
    
    def get_classroom(self,obj):
        return obj.classroom.class_name
    
    def get_session(self,obj):
        today= datetime.now().date()
        session_obj = obj.session_set.filter(active='post')
        session_serialized = SessionSerializerForLecture(session_obj,many=True)
        return session_serialized.data
    
class LectureSerializer(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()
    subject = SubjectSerializer()
    teacher = serializers.SerializerMethodField()
    classroom = ClassRoomSerializer()
    batches = BatchSerializer(many=True)

    class Meta:
        model = Lecture
        fields = ['start_time','end_time','type','subject','teacher','classroom','batches','slug','session']
    
    def get_teacher(self,obj):
        return obj.teacher.profile.name

    def get_session(self,obj):
        today= datetime.now().date()
        session_obj = obj.session_set.filter(day=today).first()
        session_serialized = SessionSerializerForLecture(session_obj)
        return session_serialized.data


class ScheduleSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()
    class Meta:
        model = Schedule
        fields = ['day','slug','lectures']

    def get_lectures(self,obj):
        lectures = obj.lecture_set.all().order_by('start_time')
        lectures_serialized = LectureSerializer(lectures,many=True)
        return lectures_serialized.data

class TimeTableSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()
    division = DivisionSerializer()

    class Meta:
        model = TimeTable
        fields = ['slug','division','schedules']

    def get_schedules(self,obj):
        schedules = obj.schedule_set.all()
        schedules_serialized = ScheduleSerializer(schedules,many=True)
        return schedules_serialized.data