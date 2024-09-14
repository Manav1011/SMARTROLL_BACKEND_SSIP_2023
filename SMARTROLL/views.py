from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import base64
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json
import secrets
from StakeHolders.models import Student,Admin,Teacher
from Profile.models import Profile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect
from Notifications.models import Event,Result
from Notifications.serializers import EventSerializer,ResultSerializer

@api_view(['GET'])
def check_server_avaibility(request):
    return JsonResponse(data={'data':True},status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token_authenticity(request):
    # we would be sending notifications details to the all eligible users in this one
    if request.user:        
        if request.user.role == 'admin':                
            # Search For Events
            admin_obj = Admin.objects.filter(profile=request.user).first()
            events = Event.objects.filter(branches__admins=admin_obj,status=True).distinct()
            events_serialized = EventSerializer(events,many=True)
            return JsonResponse(data={'data':{'Notifications':{'events':events_serialized.data}},'isAuthenticated':True},status=200)
        if request.user.role == 'teacher':                
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            events = Event.objects.filter(branches__teachers=teacher_obj,status=True).distinct()
            events_serialized = EventSerializer(events,many=True)
            return JsonResponse(data={'data':{'Notifications':{'events':events_serialized.data}},'isAuthenticated':True},status=200)
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            events = Event.objects.filter(branches__students=student_obj,status=True).distinct()
            events_serialized = EventSerializer(events,many=True)
            # get the results
            results_of_student = Result.objects.filter(student=student_obj).order_by('-created_at')
            results_of_student_serialized = ResultSerializer(results_of_student,many=True)
            return JsonResponse(data={'data':{'Notifications':{'events':events_serialized.data,'results':results_of_student_serialized.data}},'isAuthenticated':True},status=200)

def handle404(request,exception):
    return render(request,template_name='404.html')


def TeacherActivation(request,slug):    
    return render(request,'TeacherActivation.html')

def ForgotPasswordPage(request,slug):    
    return render(request,'forgotpassword.html')