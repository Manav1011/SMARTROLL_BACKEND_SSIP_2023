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
    # attendances = AttendanceSerializer(many=True)
    class Meta:
        model = Session
        fields  = ['session_id','created_at','active','lecture','student_count']
    
    def get_student_count(self,obj):
        return len(obj.attendances.all())