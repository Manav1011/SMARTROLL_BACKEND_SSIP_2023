from .models import Survey,SurveyOption,StudyMaterial
from rest_framework import serializers
from Manage.serializers import SubjectSerializer

class SurveyOptionSerializer(serializers.ModelSerializer):
    student_count = serializers.SerializerMethodField()
    submission_percentage = serializers.SerializerMethodField()

    class Meta:
        model = SurveyOption
        fields  = ['option','student_count','slug','submission_percentage']

    def get_submission_percentage(self,obj):
        allowed_students = len(obj.survey_set.first().allowed_students.all())
        if allowed_students > 0:
            marked_students = len(obj.student.all())
            submission_percentage = (marked_students * 100) / allowed_students
            return submission_percentage
        return 0
    
    def get_student_count(self,obj):
        return len(obj.student.all())

class SurveySerializer(serializers.ModelSerializer):
    options = SurveyOptionSerializer(many=True)

    class Meta:
        model = Survey
        fields  = ['title','type','options','created_at','active','slug']
        
class StudyMaterialSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = StudyMaterial
        fields = ['title','link','slug','subject']