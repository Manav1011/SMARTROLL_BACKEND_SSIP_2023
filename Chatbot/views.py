import base64
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from StakeHolders.models import Student
from Manage.models import Subject
from Session.models import Attendance
import matplotlib.pyplot as plot
import seaborn as sns

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
                        
                        # for retriving pie chart of attendance uisng matplotlib
                        attendance_data_sizes = [attendance_count, len(attendances)-attendance_count]
                        labels = ['Present','Absent']
                        colors = sns.color_palette('pastel')
                        explode = [0.05, 0]
                        
                        plot.pie(attendance_data_sizes, labels=labels,colors=colors,explode=explode,autopct='%.1f%%',startangle=60)
                        plot.title(f"{student_obj.enrollment}'s Attendance stastics for {subject_obj.subject_name}")
                        # plot.show()
                        
                        buf = BytesIO()
                        plot.savefig(buf, format='png')
                        buf.seek(0)
                        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                        buf.close()
                        
                        data['data'] = {
                            "total_lectures":len(attendances), 
                            "attended_lec":attendance_count,
                            "attendance_percentage": attendance_percentage,
                            "pie_chart_base64":image_base64
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


