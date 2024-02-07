from .models import Admin,Teacher
from rest_framework import serializers
from Manage.models import Branch,Subject
from Profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','email','ph_no']

class AdminSerializer(serializers.ModelSerializer):   
    profile = ProfileSerializer() 
    class Meta:
        model = Admin
        fields = ['id','profile']

class TeacherSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()    
    class Meta:
        model = Teacher
        fields = ['id','profile']

class TeacherProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()    
    class Meta:
        model = Teacher
        fields = ['id','profile']