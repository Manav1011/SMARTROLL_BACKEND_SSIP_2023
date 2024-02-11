from .models import Admin,Teacher,Student
from rest_framework import serializers
from Manage.serializers import BranchSerializer
from Profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','email','ph_no','role']


class AdminSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer() 
    branch = serializers.SerializerMethodField()
    class Meta:
        model = Admin
        fields = ['id','profile','branch']
    
    def get_branch(self,obj):
        branch = obj.branch_set.first()
        branches_serialized = BranchSerializer(branch)
        return branches_serialized.data

class TeacherSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()    
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['slug','profile','branch']
    
    def get_branch(self,obj):
        branch = obj.branch_set.first()
        branches_serialized = BranchSerializer(branch)
        return branches_serialized.data
    
class StudentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()    
    branch = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['slug','profile','branch']
    
    def get_branch(self,obj):
        branch = obj.branch_set.first()
        branches_serialized = BranchSerializer(branch)
        return branches_serialized.data