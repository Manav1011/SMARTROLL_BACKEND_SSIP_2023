from .models import Admin
from rest_framework import serializers
from Manage.models import Branch

class BranchOfTheAdmin(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','branch_name']

class AdminSerializer(serializers.ModelSerializer):
    branch = BranchOfTheAdmin()
    class Meta:
        model = Admin
        fields = ['id','branch']