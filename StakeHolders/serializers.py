from .models import Admin,Teacher
from rest_framework import serializers
from Manage.models import Branch,Subject
from Profile.models import Profile

class BranchOfTheAdmin(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','branch_name']

class AdminSerializer(serializers.ModelSerializer):
    branch = BranchOfTheAdmin()
    class Meta:
        model = Admin
        fields = ['id','branch']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_name','code','credit','slug']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','email','ph_no']

class TeacherSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Teacher
        fields = ['profile','subjects']