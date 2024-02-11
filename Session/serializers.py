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
    attendances = AttendanceSerializer(many=True)
    class Meta:
        model = Session
        fields  = ['session_id','created_at','active','lecture','attendances']