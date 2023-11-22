from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import base64
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import json
import secrets
from StakeHolders.models import Student
from Profile.models import Profile
from django.http import HttpResponse
from django.shortcuts import render

@api_view(['GET'])
def check_server_avaibility(request):
    return JsonResponse(data={'data':True},status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token_authenticity(request):
    return JsonResponse(data={'data':True},status=200)

@api_view(['POST'])
def student_registration(request):    
    try:           
        data = request.data['rawRequest']        
        data = json.loads(data)

        if 'q211_number' not in data or 'q208_phoneNumber' not in data or 'q207_email' not in data or 'q206_name' not in data:
            raise Exception('Please provide all the parameters')

        student_dict = data['q206_name']
        student_name = f"{student_dict['first']} {student_dict['last']}"
        student_email = data['q207_email']
        student_phone_number_dict = data['q208_phoneNumber']
        student_phone_number = f"{student_phone_number_dict['area']}{student_phone_number_dict['phone']}"    
        student_enrollment = data['q211_number']
        profile_ojb = Profile()
        profile_ojb.name = student_name
        profile_ojb.email = student_email
        profile_ojb.ph_no = student_phone_number
        profile_ojb.role = 'student'
        profile_ojb.save()
        student_obj = Student()
        student_obj.profile = profile_ojb
        student_obj.enrollment = student_enrollment
        response = {'error':False,'message':"You're account has been created successfully"}
        student_obj.thank_you_response = json.dumps(response)        
    except Exception as e:
        profile_ojb = Profile.objects.get(email=data['q207_email'])
        student_obj = Student.objects.get(profile=profile_ojb)
        response = {'error':True,'message':str(e)}
        student_obj.thank_you_response = json.dumps(response)
    finally:
        student_obj.save()

    return JsonResponse(data={'data':True},status=200)

@api_view(['POST'])
def studet_registration_response(request):            
    form_data = request.data
    if 'email' in  form_data:
        profile_obj = Profile.objects.filter(email=form_data['email']).first()
        student_obj = Student.objects.get(profile=profile_obj)
        context = json.loads(student_obj.thank_you_response)
    print(context)
    return render(request, 'studentregistration.html',context = context)

