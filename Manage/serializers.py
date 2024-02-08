from .models import Batch, Division,Semester,Subject,Branch,College
from rest_framework import serializers

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
    class Meta:
        model = Batch
        fields = ['slug','batch_name','active']


class SubjectSerializer(serializers.ModelSerializer):
    semester_number = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['slug', 'subject_name', 'code', 'credit', 'semester_number']

    def get_semester_number(self, subject):
        # Assuming you have a reverse relation from Subject to Semester named 'semesters'
        semester = subject.semester_set.get()  # Adjust this based on your actual reverse relation name

        # Assuming a subject can be associated with multiple semesters, you might want to handle this accordingly
        # For simplicity, this example assumes a single semester association
        return semester.no
        
class SemesterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Semester
        fields = ['slug','no','status','start_year','end_year']

class SemesterSerializerStudentCred(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Semester
        fields = ['slug','no','status','start_date','end_date','subjects','time_table']
