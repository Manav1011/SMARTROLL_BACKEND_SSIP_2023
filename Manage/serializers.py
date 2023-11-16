from .models import Batch,Semester
from rest_framework import serializers

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id','batch_name']

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id','no','status','start_date','end_date','subjects','time_table']