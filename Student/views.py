from django.shortcuts import render
from TimeTable.models import Timetable,Schedule,Lecture
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from StakeHolders.models import Student,Teacher
from TimeTable.serializers import ScheduleSerializer,LectureSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todays_timetable_for_student(request):
    '''
    # Get Today's Timetable for Student

    This API returns the timetable for a student based on the specified day.

    - **Method**: `GET`
    - **URL**: `/student/get_todays_timetable`
    - **Authentication**: Required (User must be logged in as a student)
    - **Permissions**: `IsAuthenticated`

    ## Input Parameters

    | Parameter | Type   | Description                |
    |-----------|--------|----------------------------|
    | `day`     | String | The day for which to fetch the timetable (e.g., "monday"). |

    ## Example Request

    ```http
    GET /student/get_todays_timetable?day=monday
    ```

    ## Response

    - **Status Code**: `200 OK`

    ```json
    {
        "lectures": [
            {
                "slug": "284527_1700595878",
                "teacher": {
                    "id": 11,
                    "profile": {
                        "name": "Dr. Mehul Parikh",
                        "email": "mehulparikh12@gmail.com",
                        "ph_no": "9312321456"
                    }
                },
                "subject": {
                    "slug": "303790_1700594968",
                    "subject_name": "Analysis And Design Of Algorithms",
                    "code": 3150703,
                    "credit": 5
                },
                "classroom": {
                    "slug": "117383_1700589406",
                    "class_name": "IT_310"
                },
                "start_time": "10:30:00",
                "end_time": "11:30:00"
            },
            {
                "slug": "188455_1700595878",
                "teacher": {
                    "id": 15,
                    "profile": {
                        "name": "BAKULBHAI PANCHAL",
                        "email": "bakulpanchal341@gmail.com",
                        "ph_no": "9878671232"
                    }
                },
                "subject": {
                    "slug": "969154_1700595011",
                    "subject_name": "Professional Ethics",
                    "code": 3150709,
                    "credit": 3
                },
                "classroom": {
                    "slug": "165259_1700589406",
                    "class_name": "IT_301"
                },
                "start_time": "11:30:00",
                "end_time": "12:30:00"
            },
            {
                "slug": "704556_1700595878",
                "teacher": {
                    "id": 18,
                    "profile": {
                        "name": "Miss. Mital Panchal",
                        "email": "mital143@gmail.com",
                        "ph_no": "9923145653"
                    }
                },
                "subject": {
                    "slug": "121681_1700595047",
                    "subject_name": "Computer Networks",
                    "code": 3150710,
                    "credit": 5
                },
                "classroom": {
                    "slug": "746537_1700589406",
                    "class_name": "IT_308"
                },
                "start_time": "14:00:00",
                "end_time": "15:00:00"
            },
            {
                "slug": "351288_1700595878",
                "teacher": {
                    "id": 20,
                    "profile": {
                        "name": "Dr. Pradip Patel",
                        "email": "pradippatel433@gmail.com",
                        "ph_no": "9878987781"
                    }
                },
                "subject": {
                    "slug": "146845_1700595081",
                    "subject_name": "Software Engineering",
                    "code": 3150711,
                    "credit": 4
                },
                "classroom": {
                    "slug": "261407_1700589406",
                    "class_name": "IT_302"
                },
                "start_time": "15:15:00",
                "end_time": "16:15:00"
            },
            null,
            null
        ]
    }
    ```

    ## Error Responses

    - **Status Code**: `500 Internal Server Error`

    ```json
    {
        "data": "Error message details"
    }
    ```

    - **Status Code**: `401 Unauthorized`

    ```json
    {
        "data": "You're not allowed to view this"
    }
    ```

    - **Status Code**: `400 Bad Request`

    ```json
    {
        "data": "Provide all the parameters"
    }
    '''
    try:
        if request.user.role == 'student':
            data = request.GET
            student = Student.objects.get(profile=request.user)            
            if 'day' not in data:
                raise ValueError('Provide all the parameters')

            timetable_obj = student.semester.time_table.get()            
            print(timetable_obj.schedules.filter(day=data['day']))
            schedule_obj = timetable_obj.schedules.filter(day=data['day']).first()
            if not schedule_obj:
                raise Exception('Schedule obj does not exist')
            all_lectures = schedule_obj.lectures.all()
            lectures = []           
            lectures = [
                LectureSerializer(lecture).data if lecture.subject in student.subjects.all() else None
                for lecture in all_lectures
            ]            
            data = {"lectures": lectures}  
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to view this")
    except Exception as e:        
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todays_timetable_for_teacher(request):
    try:
        if request.user.role == 'teacher':
            data = request.GET
            if 'day' not in data:
                raise ValueError('Provide all the parameters')
            teacher = Teacher.objects.get(profile=request.user)
            teachers_subjects = teacher.subjects.all()
            batch = teacher.branch.batches.filter(active=True).first()
            semesters = batch.semesters.filter(status=True)
            all_lectures = []
            for i in semesters:
                lecture_temp = i.time_table.get().schedules.filter(day=data['day']).first().lectures.all()
                for j in lecture_temp:
                    all_lectures.append(j)            
            lectures = [
                LectureSerializer(lecture).data if lecture.subject in teacher.subjects.all() else None
                for lecture in all_lectures
            ]
            print(lectures)
            data = {"lectures": lectures}  
            # Now get today's schedule from all the lectures            
            return JsonResponse(data,status=200)
        else:
            raise Exception("You're not allowed to view this")
    except Exception as e:        
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
