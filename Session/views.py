from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SessionSerializer
from .models import Session,Attendance
from Manage.models import Lecture
from StakeHolders.models import Student,Teacher


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lecture_session(request):
    data = {'data':None,'error':False,'message':None}
    try:
        if request.user.role == 'teacher':
            teacher_obj = Teacher.objects.filter(profile=request.user).first()
            if teacher_obj:
                body = request.data
                if 'lecture_slug' in body:
                    lecture_obj = Lecture.objects.filter(slug=body['lecture_slug']).first()
                    if lecture_obj:
                        batches = lecture_obj.batches.all()
                        lecture_session,created = Session.objects.get_or_create(lecture=lecture_obj,active=True)
                        if created:                            
                            students = Student.objects.filter(batch__in=batches)
                            for student in students:
                                attendance_obj = Attendance.objects.create(student=student)
                                lecture_session.attendances.add(attendance_obj)
                                lecture_session_serialized = SessionSerializer(lecture_session)
                                data['data'] = lecture_session_serialized.data
                        else:
                            print('already created')
                            lecture_session_serialized = SessionSerializer(lecture_session)
                            data['data'] = lecture_session_serialized.data
                        return Response(data,status=200)
                    else:
                        raise Exception('Lecture does not exists')
                else:
                    raise Exception('Parameters missing')
            else:
                raise Exception('Teacher does not exists')
        else:
            raise Exception("You're not allowed to perform this action")
    except Exception as e:
         print(e)
         data['error'] = True
         data['message'] = str(e)
         return Response(data,status=500)

         
        
          