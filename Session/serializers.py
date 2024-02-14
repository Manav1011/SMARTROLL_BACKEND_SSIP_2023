from rest_framework import serializers
from .models import Attendance,Session
from Manage.models import Batch
from Manage.serializers import LectureSerializer,BatchSerializer
from StakeHolders.serializers import StudentSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    batches = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields = ['student','is_present','marking_time','marking_ip','batches']
    def get_batches(self,obj):
        batches = Batch.objects.filter(students=obj.student)
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