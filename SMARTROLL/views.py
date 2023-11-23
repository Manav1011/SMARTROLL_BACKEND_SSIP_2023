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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect

@api_view(['GET'])
def check_server_avaibility(request):
    return JsonResponse(data={'data':True},status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_token_authenticity(request):
    return JsonResponse(data={'data':True},status=200)

def student_registration(request):
    try:
        if request.method == 'GET':
            return render(request,'studentregistration.html')
        if request.method == 'POST':
            pass
    except Exception as e:
        pass
        # raw_request = request.data.get('rawRequest')

        # if not raw_request:
        #     raise Exception('Please provide the rawRequest parameter')

        # data = json.loads(raw_request)
        # print(data)

        # required_params = ['q211_number', 'q214_phone', 'q207_email', 'q206_name']
        # if not all(param in data for param in required_params):
        #     raise Exception('Please provide all the required parameters')

        # student_name = f"{data['q206_name']['first']} {data['q206_name']['last']}"
        # student_email = data['q207_email']
        # student_phone_number = data['q214_phone']
        # student_enrollment = data['q211_number']

        # profile_obj, created = Profile.objects.get_or_create(email=student_email)
        # if created:
        #     profile_obj.name = student_name
        #     profile_obj.ph_no = student_phone_number
        #     profile_obj.role = 'student'
        #     profile_obj.is_active = True
        #     profile_obj.save()

        # student_obj, created = Student.objects.get_or_create(profile=profile_obj)
        # if not created:
        #     raise Exception('Student with this email already exists')

        # student_obj.enrollment = student_enrollment
        # response = {'error': False, 'message': "Your account has been created successfully"}
        # student_obj.thank_you_response = json.dumps(response)
        # student_obj.save()

    # except Exception as e:
    #     profile_obj = Profile.objects.get(email=data['q207_email'])
    #     student_obj = Student.objects.get(profile=profile_obj)
    #     response = {'error': True, 'message': str(e)}
    #     student_obj.thank_you_response = json.dumps(response) 
    #     student_obj.save()       

@csrf_exempt
def studet_registration_response(request):  
    if request.method == 'POST':
        form_data = request.POST
        print(form_data)
        try:
            if 'email' in  form_data:
                profile_obj = Profile.objects.filter(email=form_data['email']).first()
                student_obj = Student.objects.filter(profile=profile_obj).first()
                context = json.loads(student_obj.thank_you_response)        
                return redirect('https://356f-49-36-66-75.ngrok-free.app/#/student')
        except Exception as e:        
            return render(request, 'studentregistrationresponse.html',context = {'error':True,'message':str(e)})
    
    else:
        return render(request, 'studentregistrationresponse.html',context = {'error':True,'message':'METHOD ALLOWS: POST'})