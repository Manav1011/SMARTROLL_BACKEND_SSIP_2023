from rest_framework import serializers
from .models import Attendance,Session
from Manage.serializers import LectureSerializer
from StakeHolders.serializers import StudentSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = Attendance
        fields = ['student','is_present','marking_time','marking_ip']

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