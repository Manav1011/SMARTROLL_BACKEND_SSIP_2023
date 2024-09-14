from .models import Event,Result
from rest_framework import serializers
from Manage.serializers import BranchSerializer,SubjectSerializer
from StakeHolders.serializers import StudentSerializer

class EventSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True)
    class Meta:
        model = Event
        fields  = ['title','description','branches','status','slug']

class ResultSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    student = StudentSerializer()
    class Meta:
        model = Result
        fields  = ["total_marks","gained_marks","subject","student","remarks","created_at","slug"]

