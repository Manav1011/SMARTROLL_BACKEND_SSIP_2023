from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from Manage.models import Semester,Branch,Subject
from .models import Timetable,Schedule,Lecture,Classroom
from .serializers import TimetableSerializer,ClassRoomSerializer,LectureSerializer
from django.db import transaction
from StakeHolders.models import Admin,Teacher
from StakeHolders.serializers import TeacherProfileSerializer
from Manage.serializers import SubjectSerializer
from datetime import time

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_timetable(request):
    '''
    # Get Timetable

    Retrieve the timetable for a specific semester.

    - **URL:** `/api/get_timetable/`
    - **Method:** `GET`
    - **Permissions:** `IsAuthenticated`

    ### Request Parameters

    | Parameter      | Type   | Description                                      |
    | -------------- | ------ | ------------------------------------------------ |
    | `semester_slug` | String | (Required) Slug of the semester for the timetable |

    ### Response

    - **Status Code:** 200 OK

    ```json
    {
        "timetable": {
            "slug": "323955_1700482202",
            "schedules": [
                {
                    "slug": "190565_1700482202",
                    "day": "Monday",
                    "lecutres": [
                        {
                            "slug": "230045_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "10:30 A.M.",
                            "end_time": "11:30 A.M."
                        },
                        {
                            "slug": "134159_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "11:30 A.M.",
                            "end_time": "12:30 P.M."
                        },
                        {
                            "slug": "679348_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "01:00 P.M.",
                            "end_time": "02:00 P.M."
                        },
                        {
                            "slug": "171654_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "02:00 P.M.",
                            "end_time": "03:00 P.M."
                        },
                        {
                            "slug": "181601_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "03:15 P.M.",
                            "end_time": "04:15 P.M."
                        },
                        {
                            "slug": "129123_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "04:15 P.M.",
                            "end_time": "05:15 P.M."
                        }
                    ]
                },
                {
                    "slug": "332120_1700482202",
                    "day": "Tuesday",
                    "lecutres": [
                        {
                            "slug": "474441_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "10:30 A.M.",
                            "end_time": "11:30 A.M."
                        },
                        {
                            "slug": "725625_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "11:30 A.M.",
                            "end_time": "12:30 P.M."
                        },
                        {
                            "slug": "308887_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "01:00 P.M.",
                            "end_time": "02:00 P.M."
                        },
                        {
                            "slug": "240919_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "02:00 P.M.",
                            "end_time": "03:00 P.M."
                        },
                        {
                            "slug": "186226_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "03:15 P.M.",
                            "end_time": "04:15 P.M."
                        },
                        {
                            "slug": "160952_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "04:15 P.M.",
                            "end_time": "05:15 P.M."
                        }
                    ]
                },
                {
                    "slug": "187096_1700482202",
                    "day": "Wednesday",
                    "lecutres": [
                        {
                            "slug": "690264_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "10:30 A.M.",
                            "end_time": "11:30 A.M."
                        },
                        {
                            "slug": "224291_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "11:30 A.M.",
                            "end_time": "12:30 P.M."
                        },
                        {
                            "slug": "229898_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "01:00 P.M.",
                            "end_time": "02:00 P.M."
                        },
                        {
                            "slug": "215100_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "02:00 P.M.",
                            "end_time": "03:00 P.M."
                        },
                        {
                            "slug": "309610_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "03:15 P.M.",
                            "end_time": "04:15 P.M."
                        },
                        {
                            "slug": "288937_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "04:15 P.M.",
                            "end_time": "05:15 P.M."
                        }
                    ]
                },
                {
                    "slug": "244532_1700482202",
                    "day": "Thursday",
                    "lecutres": [
                        {
                            "slug": "200718_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "10:30 A.M.",
                            "end_time": "11:30 A.M."
                        },
                        {
                            "slug": "335506_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "11:30 A.M.",
                            "end_time": "12:30 P.M."
                        },
                        {
                            "slug": "185962_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "01:00 P.M.",
                            "end_time": "02:00 P.M."
                        },
                        {
                            "slug": "199223_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "02:00 P.M.",
                            "end_time": "03:00 P.M."
                        },
                        {
                            "slug": "653790_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "03:15 P.M.",
                            "end_time": "04:15 P.M."
                        },
                        {
                            "slug": "231254_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "04:15 P.M.",
                            "end_time": "05:15 P.M."
                        }
                    ]
                },
                {
                    "slug": "163264_1700482202",
                    "day": "Friday",
                    "lecutres": [
                        {
                            "slug": "304335_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "10:30 A.M.",
                            "end_time": "11:30 A.M."
                        },
                        {
                            "slug": "126432_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "11:30 A.M.",
                            "end_time": "12:30 P.M."
                        },
                        {
                            "slug": "257254_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "01:00 P.M.",
                            "end_time": "02:00 P.M."
                        },
                        {
                            "slug": "211586_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "02:00 P.M.",
                            "end_time": "03:00 P.M."
                        },
                        {
                            "slug": "125316_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "03:15 P.M.",
                            "end_time": "04:15 P.M."
                        },
                        {
                            "slug": "124419_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "04:15 P.M.",
                            "end_time": "05:15 P.M."
                        }
                    ]
                },
                {
                    "slug": "764860_1700482202",
                    "day": "Saturday",
                    "lecutres": [
                        {
                            "slug": "141595_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "10:30 A.M.",
                            "end_time": "11:30 A.M."
                        },
                        {
                            "slug": "217835_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "11:30 A.M.",
                            "end_time": "12:30 P.M."
                        },
                        {
                            "slug": "224635_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "01:00 P.M.",
                            "end_time": "02:00 P.M."
                        },
                        {
                            "slug": "280809_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "02:00 P.M.",
                            "end_time": "03:00 P.M."
                        },
                        {
                            "slug": "522751_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "03:15 P.M.",
                            "end_time": "04:15 P.M."
                        },
                        {
                            "slug": "183651_1700482202",
                            "subject": null,
                            "classroom": null,
                            "start_time": "04:15 P.M.",
                            "end_time": "05:15 P.M."
                        }
                    ]
                }
            ]
        }
    }
    ```

    ### Errors

    - **Status Code:** 400 Bad Request

    ```json
    {
    "data": "Please provide a valid semester slug"
    }
    ```

    - **Status Code:** 401 Unauthorized

    ```json
    {
    "data": "You're not allowed to perform this action"
    }
    ```

    - **Status Code:** 500 Internal Server Error

    ```json
    {
    "data": "An error occurred while processing the request"
    }
    ```

    ```
    Note: Replace `/api/get_timetable/` with the actual URL endpoint.
    '''
    try:
        if request.user.role == 'admin':
            body = request.GET
            if 'semester_slug' not in body:
                raise Exception('Please provide a valid semester slug')
            semester_obj = Semester.objects.get(slug=body.get('semester_slug'))
            if semester_obj:
                # Make the time table
                time_table = semester_obj.time_table.all().first()
                if time_table:                    
                    time_table_serialized = TimetableSerializer(time_table)
                    data = {"timetable":time_table_serialized.data}
                else:
                    with transaction.atomic():
                        # We have to make a new timetable
                        time_table_obj = Timetable()
                        time_table_obj.save()  # Save the Timetable instance
                        # Make 7 new schedule objects
                        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                        for i in days:
                            schedule_obj = Schedule(day=i)
                            schedule_obj.save()
                            time_table_obj.schedules.add(schedule_obj)
                            time_deltas = [(time(hour=10,minute=30,second=0),time(hour=11,minute=30,second=0)),(time(hour=11,minute=30,second=0),time(hour=12,minute=30,second=0)),(time(hour=13,minute=0,second=0),time(hour=14,minute=0,second=0)),(time(hour=14,minute=0,second=0),time(hour=15,minute=0,second=0)),(time(hour=15,minute=15,second=0),time(hour=16,minute=15,second=0)),(time(hour=16,minute=15,second=0),time(hour=17,minute=15,second=0))]
                            for j in time_deltas:                      
                                lecture_obj = Lecture(start_time = j[0],end_time = j[1])                                
                                lecture_obj.save()  # Save the Lecture instance
                                schedule_obj.lectures.add(lecture_obj)
                        semester_obj.time_table.add(time_table_obj)
                    time_table_serialized = TimetableSerializer(time_table_obj)
                    data = {"timetable":time_table_serialized.data}
                return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_objects_for_lecture(request):
    '''
    ### Get Objects for Lecture

    #### Endpoint:

    - **Method:** GET
    - **URL:** `/api/get_objects_for_lecture/`

    #### Authentication:

    - Requires authentication with a valid token.

    #### Permissions:

    - Requires the user to have the 'admin' role.

    #### Parameters:

    - `semester_slug` (string, required): The slug of the semester for which objects are requested.

    #### Response:

    ```json
    {
        "subjects": [
            {
                "slug": "169719_1700459626",
                "subject_name": "Analysis And Design Of Algorithms",
                "code": 3150703,
                "credit": 5,
                "teachers": [
                    {
                        "id": 5,
                        "profile": {
                            "name": "Shraddha Modi",
                            "email": "shraddhamodi@gmail.com",
                            "ph_no": "9925717005"
                        }
                    },
                    {
                        "id": 3,
                        "profile": {
                            "name": "kishan nurani",
                            "email": "kishan@gmail.com",
                            "ph_no": "919925717005"
                        }
                    }
                ]
            },
            {
                "slug": "317463_1700459688",
                "subject_name": "Professional Ethics",
                "code": 3150709,
                "credit": 3,
                "teachers": [
                    {
                        "id": 1,
                        "profile": {
                            "name": "Pragnesh Patel",
                            "email": "pragneshpatel@gmail.com",
                            "ph_no": "919925717005"
                        }
                    }
                ]
            },
            {
                "slug": "276506_1700459713",
                "subject_name": "Computer Networks",
                "code": 3150710,
                "credit": 5,
                "teachers": [
                    {
                        "id": 3,
                        "profile": {
                            "name": "kishan nurani",
                            "email": "kishan@gmail.com",
                            "ph_no": "919925717005"
                        }
                    }
                ]
            },
            {
                "slug": "465827_1700459730",
                "subject_name": "Software Engineering",
                "code": 3150711,
                "credit": 5,
                "teachers": [
                    {
                        "id": 2,
                        "profile": {
                            "name": "vimal vaghela",
                            "email": "vimalvaghela@gmail.com",
                            "ph_no": "7874032915"
                        }
                    }
                ]
            },
            {
                "slug": "318459_1700472974",
                "subject_name": "Python for Data Science",
                "code": 3150713,
                "credit": 3,
                "teachers": []
            },
            {
                "slug": "183385_1700473124",
                "subject_name": " Cyber Security",
                "code": 3150714,
                "credit": 2,
                "teachers": [
                    {
                        "id": 5,
                        "profile": {
                            "name": "Shraddha Modi",
                            "email": "shraddhamodi@gmail.com",
                            "ph_no": "9925717005"
                        }
                    }
                ]
            }
        ],
        "classrooms": [
            {
                "slug": "492036_1700305422",
                "class_name": "CE_101"
            },
            {
                "slug": "215962_1700305439",
                "class_name": "CE_102"
            },
            {
                "slug": "103216_1700305454",
                "class_name": "CE_103"
            },
            {
                "slug": "179211_1700305529",
                "class_name": "CE_104"
            },
            {
                "slug": "219981_1700305543",
                "class_name": "CE_105"
            },
            {
                "slug": "752835_1700305558",
                "class_name": "CE_106"
            },
            {
                "slug": "117893_1700305579",
                "class_name": "CE_107"
            },
            {
                "slug": "247468_1700305592",
                "class_name": "CE_108"
            },
            {
                "slug": "428503_1700305639",
                "class_name": "CE_109"
            },
            {
                "slug": "968839_1700305653",
                "class_name": "CE_110"
            }
        ]
    }
    ```

    #### Status Codes:

    - 200 OK: Successfully retrieved objects.
    - 401 Unauthorized: User does not have the required role.
    - 500 Internal Server Error: An error occurred on the server.
    '''
    try:
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            body = request.GET
            if 'semester_slug' not in body:
                raise Exception('Please provide valid semester slug')
            semester_obj = Semester.objects.get(slug=body['semester_slug'])
            subjects_obj = semester_obj.subjects.all()
            subjects = []
            for i in subjects_obj:
                subject_obj = SubjectSerializer(i)
                subject_obj_serialized = subject_obj.data
                teachers_obj = TeacherProfileSerializer(i.teacher_set.all(),many=True)
                subject_obj_serialized['teachers'] = teachers_obj.data
                subjects.append(subject_obj_serialized)            
            classrooms = Classroom.objects.filter(branch=branch_obj).all()
            classrooms_serialized = ClassRoomSerializer(classrooms,many=True)            
            data = {
                'subjects':subjects,
                'classrooms':classrooms_serialized.data,                
            }
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_lecture_attributes(request):
    '''
    ### Set Lecture Attributes

    #### Endpoint:

    - **Method:** POST
    - **URL:** `/api/set_lecture_attributes/`

    #### Authentication:

    - Requires authentication with a valid token.

    #### Permissions:

    - Requires the user to have the 'admin' role.

    #### Parameters:

    - `lecture_slug` (string, required): The slug of the lecture for which attributes are to be set.
    - `teacher_id` (integer, required): The ID of the teacher to assign to the lecture.
    - `subject_slug` (string, required): The slug of the subject to assign to the lecture.
    - `classroom_slug` (string, required): The slug of the classroom to assign to the lecture.

    #### Response:

    ```json
    {
        "lecture": {
            "slug": "216906_1700490876",
            "teacher": 5,
            "subject": {
                "slug": "169719_1700459626",
                "subject_name": "Analysis And Design Of Algorithms",
                "code": 3150703,
                "credit": 5
            },
            "classroom": {
                "slug": "492036_1700305422",
                "class_name": "CE_101"
            },
            "start_time": "04:15 P.M.",
            "end_time": "05:15 P.M."
        }
    }
    ```

    #### Status Codes:

    - 200 OK: Lecture attributes set successfully.
    - 401 Unauthorized: User does not have the required role.
    - 500 Internal Server Error: An error occurred on the server.
    '''
    try:
        if request.user.role == 'admin':
            body = request.data
            if 'lecture_slug' not in body:
                raise Exception('parameters Missing!')
            if 'teacher_id' not in body:
                raise Exception('parameters Missing!')
            if 'subject_slug' not in body:
                raise Exception('parameters Missing!')
            if 'classroom_slug' not in body:
                raise Exception('parameters Missing!')

            with transaction.atomic():
                lecture_obj = Lecture.objects.get(slug=body['lecture_slug'])
                teacher_obj = Teacher.objects.get(id=body['teacher_id'])
                subject_obj = Subject.objects.get(slug = body['subject_slug'])
                classroom_obj = Classroom.objects.get(slug=body['classroom_slug'])
                lecture_obj.teacher = teacher_obj
                lecture_obj.subject = subject_obj
                lecture_obj.classroom = classroom_obj
                lecture_obj.save()
            lecture_obj_serialized = LectureSerializer(lecture_obj)
            return JsonResponse(data={'lecture':lecture_obj_serialized.data},status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)