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
        
        
# class SubjectSerializer(serializers.ModelSerializer):
#     semester = serializers.SerializerMethodField()

#     class Meta:
#         model = Subject
#         fields = ['slug', 'subject_name', 'code', 'credit', 'semester']

#     def get_semester(self, subject):
#         semester = subject.semester_set.first()
#         if semester:
#             return {
#                 'slug': semester.slug,
#                 'no': semester.no,
#                 'status': semester.status,
#                 'start_date': semester.start_date,
#                 'end_date': semester.end_date,
#                 'time_table': list(semester.time_table.values()),  # Adjust based on your TimeTable model
#             }
#         else:
#             return None

        
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
