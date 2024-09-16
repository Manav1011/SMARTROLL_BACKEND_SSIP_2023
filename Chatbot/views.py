import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plot
import seaborn as sns
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from StakeHolders.models import Student
from Manage.models import Subject
from Session.models import Attendance
from Notifications.models import Result
from Notifications.serializers import ResultSerializer

# Create your views here.

@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_student_attendance_detail_for_subject(request,subject_slug):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()            
            if student_obj:
                subject_obj = Subject.objects.filter(slug=subject_slug).first()
                if subject_obj:
                    attendances = Attendance.objects.filter(session__lecture__subject=subject_obj,student=student_obj)
                    if attendances:
                        attendance_count = attendances.filter(is_present=True).count()
                        attendance_percentage = (attendance_count/len(attendances))*100
                        
                        # # for retriving pie chart of attendance uisng matplotlib
                        # attendance_data_sizes = [attendance_count, len(attendances)-attendance_count]
                        # labels = ['Present','Absent']
                        # colors = sns.color_palette(['#90EE90', '#FFCCCB'])
                        # explode = [0.05, 0]
                        # print(attendance_data_sizes[1])
                        
                        # if attendance_data_sizes[1] == 0:
                        #     print('hoe')
                        #     plot.pie([attendance_data_sizes[0]], labels=['Present'],colors=colors,autopct='%.1f%%',startangle=60)
                        # elif attendance_data_sizes[0] == 0:
                        #     print('boe')
                        #     plot.pie([attendance_data_sizes[1]], labels=['Absent'],colors=colors,autopct='%.1f%%',startangle=60)
                        # else:
                        #     print('hey')
                        #     plot.pie(attendance_data_sizes, labels=labels,colors=colors,explode=explode,autopct='%.1f%%',startangle=60)
                        # plot.title(f"{student_obj.enrollment}'s Attendance stastics for {subject_obj.subject_name}")

                        # #create base64 of graph without saving it on disk 
                        # buf = BytesIO()
                        # plot.savefig(buf, format='png')
                        # buf.seek(0)
                        # image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                        # buf.close()
                        
                        data['data'] = {
                            "total_lectures":len(attendances), 
                            "attended_lec":attendance_count,
                            "attendance_percentage": attendance_percentage,
                            # "pie_chart_base64":image_base64
                            }
                        return Response(data,status=200)
                    else:
                        raise Exception('There is no lecture for this subject till now!!')
                else:
                    raise Exception('Subject does not exist!!')
            else:
                raise Exception('Student does not exist!!')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)

@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def get_result_of_student_by_subject(request,subject_slug):
    data = {'data':None,'error':False,'message':None,"code":None}
    try:
        if request.user.role == 'student':
            student_obj = Student.objects.filter(profile=request.user).first()            
            if student_obj:
                subject_obj = Subject.objects.filter(slug=subject_slug).first()
                if subject_obj:
                    results_of_student = Result.objects.filter(student=student_obj,subject=subject_obj)
                    if results_of_student:
                        results_of_student_serialized = ResultSerializer(results_of_student,many=True)
                        data['data'] = results_of_student_serialized.data
                        return Response(data,status=200)
                    else:
                        raise Exception('Result of this subject is not available!!')
                else:
                    raise Exception('Subject does not exist!!')
            else:
                raise Exception('Student does not exist!!')
        else:
            raise Exception("You're not allowed to perform this action!!")
    except Exception as e:
        print(e)
        data['error'] = True
        data['message'] = str(e)
        return Response(data,status=500)