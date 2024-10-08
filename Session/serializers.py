from rest_framework import serializers
from .models import Attendance,Session,Survey,SurveyOption
from Manage.models import Batch
from Manage.serializers import LectureSerializer,BatchSerializer
from StakeHolders.serializers import StudentSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    batches = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields = ['slug','student','is_present','marking_time','batches','manual']
    def get_batches(self,obj):
        batches = obj.session_set.first().lecture.batches.filter(students=obj.student)
        batches_serialized = BatchSerializer(batches,many=True)
        return batches_serialized.data
        

class SessionSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer()
    student_count = serializers.SerializerMethodField()
    marked_attendances = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields  = ['session_id','created_at','active','lecture','student_count','marked_attendances']
    
    def get_student_count(self,obj):
        return len(obj.attendances.all())

    def get_marked_attendances(self,obj):
        attendances_marked = obj.attendances.filter(is_present=True)
        attendances_serialized = AttendanceSerializer(attendances_marked,many=True)
        return attendances_serialized.data
    
class SessionSerializerHistory(serializers.ModelSerializer):
    lecture = LectureSerializer()
    student_count = serializers.SerializerMethodField()
    marked_attendances = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields  = ['session_id','day','created_at','active','lecture','student_count','marked_attendances']
    
    def get_student_count(self,obj):
        return len(obj.attendances.all())

    def get_marked_attendances(self,obj):
        attendances_marked = obj.attendances.all()
        attendances_serialized = AttendanceSerializer(attendances_marked,many=True)
        return attendances_serialized.data

class SurveyOptionSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    submission_percentage = serializers.SerializerMethodField()

    class Meta:
        model = SurveyOption
        fields  = ['option','student_count','slug','submission_percentage']

    def get_submission_percentage(self,obj):
        allowed_students = len(obj.survey_set.first().allowed_students.all())
        marked_students = len(obj.student.all())
        submission_percentage = (marked_students * 100) / allowed_students
        return submission_percentage
    
    def get_student_count(self,obj):
        return len(obj.student.all())

class SurveySerializer(serializers.ModelSerializer):
    options = SurveyOptionSerializer(many=True)

    class Meta:
        model = Survey
        fields  = ['title','type','allowd_choices','options','created_at','active','slug']
        