from .models import Batch,Semester,Subject,Branch
from rest_framework import serializers

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['branch_name','slug']

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['slug','batch_name','active']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['slug','subject_name','code','credit']

        
class SemesterSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Semester
        fields = ['slug','no','status','start_date','end_date','subjects','time_table']

class SemesterSerializerStudentCred(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Semester
        fields = ['slug','no','status','start_date','end_date','subjects','time_table']
