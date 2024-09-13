from turtle import title
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Survey,SurveyOption, StudyMaterial
from StakeHolders.models import Teacher,Student
from Manage.models import Branch,Semester,Division,Batch,Subject,Lecture
from .serializers import SurveySerializer,StudyMaterialSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_survey_for_a_lecture(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                print(teacher_obj.slug)
                body = request.data   
                if 'survey_title' in body and 'type' in body and 'options' in body and 'branch_slug' in body and 'semester_slug' and 'division_slug' in body and 'batch_slug' in body:
                    branch_obj = Branch.objects.filter(slug=body['branch_slug']).first()
                    if branch_obj:
                        active_term = branch_obj.term_set.filter(status=True).first()
                        # The survey is for the whole branch
                        survey_obj = Survey.objects.create(title=body['survey_title'],type=body['type'],owner=teacher_obj)
                        for option in body['options']:
                            option_obj = SurveyOption.objects.create(option=option)
                            survey_obj.options.add(option_obj)

                        # Filtering the allowd students for the survey
                        if body['semester_slug'] == '''__all__''':    
                            # We need to get every student from the branch
                            students = Student.objects.filter(batch__division__semester__term=active_term).distinct()
                            survey_obj.allowed_students.add(*students)                            
                        
                        elif body['division_slug'] == '''__all__''':                            
                            semester_obj = Semester.objects.filter(slug=body['semester_slug']).first()
                            students = Student.objects.filter(batch__division__semester=semester_obj).distinct()
                            survey_obj.allowed_students.add(*students)
                        
                        elif body['batch_slug'] == '''__all__''':
                            division_obj = Division.objects.filter(slug=body['division_slug']).first()
                            students = Student.objects.filter(batch__division=division_obj).distinct()
                            survey_obj.allowed_students.add(*students)                            
                        
                        else:                            
                            batch_obj = Batch.objects.filter(slug=body['batch_slug']).first()
                            students = Student.objects.filter(batch=batch_obj).distinct()
                            survey_obj.allowed_students.add(*students)
                        
                        
                        survey_serialized = SurveySerializer(survey_obj)
                        data['data'] = survey_serialized.data
                        return Response(data,status=200)
                    
                    else:
                        raise Exception('Branch does not exist')
                else:
                    raise Exception('Parameters Missing')
            else:
                raise Exception('Teacher does not exist')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)

@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_surveys_of_the_teacher(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()            
            if teacher_obj:
                surveys = Survey.objects.filter(owner=teacher_obj)
                survey_serialized = SurveySerializer(surveys,many=True)
                data['data'] = survey_serialized.data
                return Response(data,status=200)
            else:
                raise Exception('Teacher does not exists')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)
    
@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_surveys_of_the_student(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()            
            if student_obj:
                surveys = Survey.objects.filter(allowed_students=student_obj)
                survey_serialized = SurveySerializer(surveys,many=True)
                data['data'] = survey_serialized.data
                return Response(data,status=200)
            else:
                raise Exception('Student does not exist')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_survey(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()
            if student_obj:
                body = request.data
                if 'survey_slug' in body and 'marked_option_slug' in body:
                    survey_obj = Survey.objects.filter(slug=body['survey_slug']).first()
                    if survey_obj:
                        # Check if student is eligible for marking the survey
                        if survey_obj.allowed_students.contains(student_obj):
                            marked_option_obj = survey_obj.options.filter(slug=body['marked_option_slug']).first()
                            if marked_option_obj:                                
                                rest_of_the_options = survey_obj.options.all().exclude(id=marked_option_obj.id)
                                for option in rest_of_the_options:
                                    if option.student.contains(student_obj):
                                        # option.student.remove(student_obj)
                                        raise Exception("You've already marked your choice!!")  
                                marked_option_obj.student.add(student_obj)
                                data['message'] = "You're submission has been successfully marked!!"
                                return Response(data,status=200)
                            else:
                                raise Exception("Marked option does not exist")
                        else:
                            raise Exception("You're not eligible for marking this survey")
                    else:
                        raise Exception('Survey does not exist')
            else:
                raise Exception('Student does not exist')
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_study_material(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                body = request.data  
                if 'material_title' in body and 'material_link' in body and 'subject_slug' in body:
                    subject_obj = Subject.objects.filter(slug=body['subject_slug']).first()
                    if subject_obj:
                        if subject_obj.lecture_set.filter(teacher=teacher_obj).exists():
                            study_material_obj = StudyMaterial.objects.create(title=body['material_title'],link=body['material_link'],subject=subject_obj,owner=teacher_obj)
                            study_material_serialized = StudyMaterialSerializer(study_material_obj)
                            data['data'] = study_material_serialized.data
                            return Response(data,status=200)
                        else:
                            raise Exception("It's not taken by you for now!!")
                    else:
                        raise Exception("Subject does not exist ")   
                else:
                    raise Exception('Parameters Missing')     
            else:
                raise Exception('Teacher does not exist')        
        else:
            raise Exception("You're not allowed to perform this action!!")      
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)
  
@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_study_material_for_teachers(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()            
            if teacher_obj:
                study_materials = StudyMaterial.objects.filter(owner=teacher_obj)
                study_material_serialized = StudyMaterialSerializer(study_materials,many=True)
                data['data'] = study_material_serialized.data
                return Response(data,status=200)
            else:
                raise Exception('Teacher does not exist')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)  
     
@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_study_material_for_students(request):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()            
            if student_obj:
                study_materials = StudyMaterial.objects.filter(subject__semester__division__batch__students=student_obj)
                study_material_serialized = StudyMaterialSerializer(study_materials,many=True)
                data['data'] = study_material_serialized.data
                return Response(data,status=200)
            else:
                raise Exception('Student does not exist')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)