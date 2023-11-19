from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from StakeHolders.models import Admin,Teacher
from .serializers import BatchSerializer,SemesterSerializer,SubjectSerializer
from StakeHolders.serializers import TeacherSerializer
from rest_framework.views import APIView
from Manage.models import Batch,Semester,Subject
from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_object_counts(request):
    '''
    # Get Object Counts API

    **Endpoint:** `/api/get_object_counts/`

    **HTTP Method:** `GET`

    **Authorization:** Token-based authentication (Authorization header required)

    ## Description
    This API retrieves counts of various objects based on the user's role.

    ## Authentication
    - **Token:** This endpoint requires a valid user token. Include the token in the "Authorization" header of the request.

    ## Request

    ### Headers
    - **Authorization:** `Token YOUR_TOKEN`

    ## Response

    ### Success Response (200 OK)

    ```json
    {
    "batches": 3,
    "teachers": 10,
    "semesters": 15,
    "subjects": 40
    }
    ```

    ### Error Response (401 Unauthorized)

    ```json
    {
    "data": "You're not allowed to perform this action"
    }
    ```

    ### Error Response (401 Unauthorized - Token not provided)

    ```json
    {
    "detail": "Authentication credentials were not provided."
    }
    ```

    ### Error Response (401 Unauthorized - Token is invalid or expired)

    ```json
    {
    "detail": "Invalid token."
    }
    ```

    ### Error Response (500 Internal Server Error)

    ```json
    {
    "data": "Internal server error occurred."
    }
    ```

    ## Notes
    - Only users with the "admin" role are allowed to access this API.
    '''
    try:        
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            # Admin exclusive fields will be here
            branch_obj = admin_obj.branch
            # Count the batches in particular branch - from branch
            batch_obj = branch_obj.batches.all()
            batches_count = batch_obj.count()
            # Count semesters in each batches - from batches
            semesters = []
            for i in batch_obj:
                semesters_obj = i.semesters.all()
                for j in semesters_obj:
                    semesters.append(j)
            semesters_count = len(semesters)
            # Count Subjects in each semesters - from semester
            subjects = []
            for i in semesters:
                subjects_obj = i.subjects.all()
                for j in subjects_obj:
                    subjects.append(j)
            subjects_count = len(subjects)
            # Count teachers in the branch - from reverse query on branch
            teachers = Teacher.objects.filter(branch=branch_obj)
            teachers_count = teachers.count()            
            data = {'batches':batches_count,'teachers':teachers_count,'semesters':semesters_count,'subjects':subjects_count}
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batches(request):     
    ''' 
    ### Get Batches

    **Description:** Retrieve a list of batches associated with the admin's branch.

    **Endpoint:** `/get_batches`

    **Method:** `GET`

    **Permissions:** `IsAuthenticated`

    **Request:**

    No request parameters are required.

    **Response:**

    - `200 OK`: Successfully retrieved batches.
    ```json
    {
        "batches": [
        {
            "id": 1,
            "batch_name": "Batch A",
            "semesters": [1, 2]
        },
        {
            "id": 2,
            "batch_name": "Batch B",
            "semesters": [3, 4]
        }
        // ... other batches
        ]
    }
    ```

    - `204 No Content`: No active batches found.
    ```json
    {
        "data": "Currently there are no active batches"
    }
    ```

    - `401 Unauthorized`: User does not have permission.
    ```json
    {
        "data": "You're not allowed to perform this action"
    }
    ```

    ---
    '''
    try:        
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            batches = branch_obj.batches.all()            
            if batches.exists():                            
                batch_serialized_obj = BatchSerializer(batches,many=True)
                data = {'data':batch_serialized_obj.data}
                return JsonResponse(data,status=200)
            else:                
                data = {"data":"Currently there are no active batches"}
                return JsonResponse(data,status=500)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batches(request):
    '''    
    ### Add Batch

    **Description:** Add a new batch to admin's branch.

    **Endpoint:** `/add_batch`

    **Method:** `POST`

    **Permissions:** `IsAuthenticated`

    **Request:**

    - Body:
    - `batch_name` (string, required): Name of the new batch.

    **Response:**

    - `200 OK`: Successfully added a new batch.
    ```json
    {
        "data": {
        "id": 3,
        "batch_name": "New Batch"    
        }
    }
    ```

    - `422 Unprocessable Entity`: Parameters missing or invalid.
    ```json
    {
        "data": "parameters missing"
    }
    ```

    - `401 Unauthorized`: User does not have permission.
    ```json
    {
        "data": "You're not allowed to perform this action"
    }
    '''
    try:
        if request.user.role == 'admin':
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)
            if body.get('batch_name') and len(body['batch_name']) > 0:
                batch_obj = Batch.objects.create(batch_name=body['batch_name'])            
                admin_obj.branch.batches.add(batch_obj)            
                batch_serialized_obj = BatchSerializer(batch_obj,many=False)            
                data = {'data':batch_serialized_obj.data}
                return JsonResponse(data,status=200)
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=401)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_semesters(request):
    '''
    # Get Semesters API

    **Endpoint:** `/get_semesters`

    **Method:** `GET`

    **Permissions:** `IsAuthenticated`

    ## Description

    Retrieve a list of semesters associated with a specific batch.

    ## Request

    ### Query Parameters

    - `batch_slug` (string, required): Slug of the batch for which semesters are to be retrieved.

    ## Response

    - `200 OK`: Successfully retrieved semesters.

    ```json
    {
        "data": [
        {
            "id": 1,
            "no": 1,
            "subjects": [],
            "timetable":[],
            "status": 1,
            "start_date": "2023-01-01",
            "end_date": "2023-06-30"
        },
        {
            "id": 2,
            "no": 2,
            "subjects": [],
            "timetable":[],
            "status": 1,
            "start_date": "2023-07-01",
            "end_date": "2023-12-31"
        }      
        ]
    }
    ```

    - `204 No Content`: No active semesters found.

    ```json
    {
        "data": "Currently there are no active semesters in this batch"
    }
    ```

    - `401 Unauthorized`: User does not have permission.

    ```json
    {
        "data": "You're not allowed to perform this action"
    }
    ```

    - `422 Unprocessable Entity`: Invalid or missing parameters.

    ```json
    {
        "data": "Invalid or missing batch_id parameter"
    }
    ```

    - `500 Internal Server Error`: Server error occurred.

    ```json
    {
        "data": "Internal Server Error: <error_message>"
    }
    ```
    '''
    try:
        if request.user.role == 'admin':
            body = request.GET
            admin_obj = Admin.objects.get(profile=request.user)
            if body.get('batch_slug') and len(body['batch_slug']) > 0:
                batch_obj = admin_obj.branch.batches.get(slug=body['batch_slug'])        
                if batch_obj:
                    semesters = batch_obj.semesters
                    if semesters.exists():
                        semesters_serialized = SemesterSerializer(semesters,many=True)
                        data = {'data':semesters_serialized.data}
                        return JsonResponse(data,status=200)
                    else:
                        data = {"data":"Currently there are no active semesters in this batch"}
                        return JsonResponse(data,status=500)               
                else:
                    raise Exception('Batch does not found')
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_semester(request):
    '''
    # Add Semester

    **Description:** Add a new semester to a batch.

    **Endpoint:** `/add_semester`

    **Method:** `POST`

    **Permissions:** `IsAuthenticated`

    **Request:**

    - Body:
    - `batch_slug` (string, required): Slug of the batch to which the semester will be added.
    - `semester_number` (integer, required): Semester number.
    - `start_date` (string, required): Start date of the semester in the format 'YYYY-MM-DD'.
    - `end_date` (string, required): End date of the semester in the format 'YYYY-MM-DD'.

    **Response:**

    - `200 OK`: Successfully added a new semester.
    ```json
    {
        "data": {
            "id": 1,
            "no": 1,
            "start_date": "2023-01-01",
            "end_date": "2023-05-31"
        }
    }
    ```

    - `422 Unprocessable Entity`: Parameters missing or invalid.
    ```json
    {
        "data": "parameters missing"
    }
    ```

    - `401 Unauthorized`: User does not have permission.
    ```json
    {
        "data": "You're not allowed to perform this action"
    }
    ```

    - `500 Internal Server Error`: An unexpected error occurred.
    ```json
    {
        "data": "Error message"
    }
    ```
    '''
    try:
        if request.user.role == 'admin':
            body = request.data            
            if body.get('batch_slug') and len(body['batch_slug']) > 0 and body.get('semester_number') and int(body['semester_number']) > 0 and body.get('start_date') and body.get('end_date'):
                batch_obj = Batch.objects.get(slug = body['batch_slug'])
                if batch_obj:
                    if batch_obj.semesters.filter(no=body['semester_number']):
                        raise Exception('Please add a unique semester')
                    start = datetime.strptime(body.get('start_date'), '%Y-%m-%d').date()
                    end = datetime.strptime(body.get('end_date'), '%Y-%m-%d').date()
                    semester_obj = Semester(no=body['semester_number'],start_date=start,end_date=end)
                    semester_obj.save()
                    batch_obj.semesters.add(semester_obj)
                    semester_serialized_obj = SemesterSerializer(semester_obj,many=False)            
                    data = {'data':semester_serialized_obj.data}
                    return JsonResponse(data,status=200)
                else:
                    raise Exception('batch not found')                    
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subjects(request):
    '''
    # Get Subjects API

    ## Description

    Retrieve a list of subjects associated with a specific semester.

    ## Endpoint

    `GET /get_subjects`

    ## Method

    `GET`

    ## Permissions

    - `IsAuthenticated`

    ## Request

    | Parameter      | Type   | Description                                  |
    | -------------- | ------ | -------------------------------------------- |
    | `semester_slug`| String | (Required) Slug of the target semester.       |    

    ## Response

    - `200 OK`: Successfully retrieved subjects.
    ```json
    {
        "data": [
            {
                "id": 1,
                "name": "Subject A",
                "code": "SUBA101",
                "credit": 3
            },
            {
                "id": 2,
                "name": "Subject B",
                "code": "SUBB201",
                "credit": 4
            }
            // ... other subjects
        ]
    }
    ```

    - `204 No Content`: No active subjects found.
    ```json
    {
        "data": "Currently there are no active subjects in this semester"
    }
    ```

    - `401 Unauthorized`: User does not have permission.
    ```json
    {
        "data": "You're not allowed to perform this action"
    }
    ```

    - `422 Unprocessable Entity`: Parameters missing or invalid.
    ```json
    {
        "data": "parameters missing"
    }
    ```

    - `500 Internal Server Error`: Exception occurred.
    ```json
    {
        "data": "Error message here"
    }
    ```
    '''
    try:
        if request.user.role == 'admin':
            body = request.GET            
            if body.get('semester_slug') and len(body['semester_slug']) > 0:
                semester_obj = Semester.objects.get(slug=body.get('semester_slug'))
                if semester_obj:
                    subjects = semester_obj.subjects
                    if subjects.exists():
                        subjects_serialized = SubjectSerializer(subjects,many=True)
                        data = {'data':subjects_serialized.data}
                        return JsonResponse(data,status=200)
                    else:
                        data = {"data":"Currently there are no active subjects in this semester"}
                        return JsonResponse(data,status=500)               
                else:
                    raise Exception('Semester does not found')
            else:
                data = {'data':'parameters missing'}
                return JsonResponse(data,status=422)            
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_subjects(request):
    '''
    # Add Subject to Semester API

    **Endpoint:** `/api/add_subject_to_semester/`

    ### Description

    This API allows an admin to add a new subject to a specific semester.

    ### Warning

    - Ensure that the semester exists before attempting to add a subject.
    - Verify that the subject with the given code is not already added to the semester.

    ### Request

    - **Method:** `POST`
    - **Authentication:** Required (Admin)

    ### Parameters

    | Parameter        | Type     | Description                                     |
    |------------------|----------|-------------------------------------------------|
    | `semester_slug`  | String   | (Required) Slug of the target semester.         |
    | `subject_name`   | String   | (Required) Name of the new subject.             |
    | `subject_code`   | String   | (Required) Code of the new subject.             |
    | `subject_credit` | Integer  | (Required) Credit hours for the new subject.    |

    ### Example Request

    ```json
    {
    "semester_slug": "your-semester-slug",
    "subject_name": "New Subject",
    "subject_code": "NS101",
    "subject_credit": 3
    }
    ```

    ### Response

    - **Status Code:** `200 OK`
    - **Data Format:** JSON

    ```json
    {
    "subject": {
        "id": 1,
        "subject_name": "New Subject",
        "code": "NS101",
        "credit": 3
        // ... (other subject fields)
    }
    }
    ```

    ### Possible Errors

    - **Status Code:** `401 Unauthorized`
    - **Data Format:** JSON

    ```json
    {
    "data": "You're not allowed to perform this action"
    }
    ```

    ```json
    {
    "data": "Semester does not found"
    }
    ```

    ```json
    {
    "data": "Subject is already added to the semester"
    }
    ```

    ```json
    {
    "data": "Provide all parameters"
    }
    ```

    ```json
    {
    "data": "Internal Server Error"
    }
    ```

    **Note:** Replace the placeholder values in the example request with actual data.
    '''
    try:
        if request.user.role == 'admin':
            body = request.data
            semester_slug = body['semester_slug']
            semester_obj = Semester.objects.get(slug = semester_slug)
            if semester_obj:
                if semester_obj.subjects.filter(code=body.get('subject_code')):
                        raise Exception('Subject is already added to the semester')
                if not body.get('subject_name') or not body.get('subject_code') or not body.get('subject_credit'):
                    raise Exception('Provide all parameters')
                with transaction.atomic():                               
                    subject_obj = Subject(subject_name = body.get('subject_name'),code= body.get('subject_code'),credit=body.get('subject_credit'))
                    subject_obj.save()
                    semester_obj.subjects.add(subject_obj)
                added_subject = SubjectSerializer(subject_obj,many=False)
                data = {'subject':added_subject.data}
                return JsonResponse(data,status=200)
            else:
                raise Exception('Semester does not found')
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:        
        data = {"data":str(e)}
        return JsonResponse(data,status=401)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teachers(request):
    '''
    ### Get Teachers

    Retrieve a list of teachers associated with the admin's branch.

    - **URL:** `/api/get_teachers/`
    - **Method:** `GET`
    - **Authentication:** Required (Token-based authentication)

    #### Request Parameters:

    | Parameter  | Type   | Description                             |
    |------------|--------|-----------------------------------------|
    | None       |        | No additional parameters are required.   |

    #### Response:

    - **Status Code:** 200 OK
    ```json
    {
        "teachers": [
            {
                "profile": {
                    "name": "Kishan Noorani",
                    "email": "kishan@gmail.com",
                    "ph_no": "9925717005"
                },
                "subjects": [
                    {
                        "subject_name": "Computer Networks ",
                        "code": 3150710,
                        "credit": 5,
                        "slug": "551162_1700243634"
                    }
                ]
            },
            {
                "profile": {
                    "name": "Shraddha Modi",
                    "email": "shraddhamodi@gmail.com",
                    "ph_no": "+919925717005"
                },
                "subjects": [
                    {
                        "subject_name": "Analysis And Design Of Algorithms",
                        "code": 3150703,
                        "credit": 5,
                        "slug": "223792_1700243634"
                    }
                ]
            }
        ]
    }
    ```

    - **Status Code:** 500 Internal Server Error
    ```json
    {
        "data": "Currently there are no active teachers"
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
        "data": "Internal Server Error: [error details]"
    }
    ```
    '''
    try:
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            teachers = Teacher.objects.filter(branch = branch_obj)            
            if teachers.exists():
                teachers_serialized = TeacherSerializer(teachers,many=True)
                data = {'teachers':teachers_serialized.data}
                return JsonResponse(data,status=200)
            else:
                data = {"data":"Currently there are no active teachers"}
                return JsonResponse(data,status=500)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_teacher(request):
    '''
    ## Add Teacher

    Endpoint to add a new teacher.

    - **URL:** `/add_teacher`
    - **Method:** `POST`
    - **Authentication:** Required (Token-based authentication)

    ### Request Parameters

    | Parameter | Type   | Description                               |
    |-----------|--------|-------------------------------------------|
    | email     | String | Email of the teacher (required, non-empty) |
    | password  | String | Password for the teacher (required, non-empty, at least 8 characters) |
    | name      | String | Name of the teacher (required, non-empty)  |
    | ph_no     | String | Phone number of the teacher (required, non-empty) |

    ### Response

    - **Success Response:**
    - **Status Code:** 200 OK
    - **Content:**
        ```json
        {
            "teacher": {
                "profile": {
                    "name": "Pragnesh Patel",
                    "email": "pragneshpatel@gmail.com",
                    "ph_no": "+919925717005"
                },
                "subjects": []
            }
        }
        ```

    - **Error Response:**
    - **Status Code:** 401 Unauthorized
        - **Content:**
        ```json
        {
            "data": "You're not allowed to perform this action"
        }
        ```
    - **Status Code:** 500 Internal Server Error
        - **Content:**
        ```json
        {
            "data": "An error occurred while processing your request."
        }
        ```

    ### Notes

    - The password must be at least 8 characters long.
    - The API requires token-based authentication. Ensure the user making the request has the necessary permissions.
    '''
    try:
        if request.user.role == 'admin':
            admin_obj = Admin.objects.get(profile=request.user)
            branch_obj = admin_obj.branch
            body = request.data
            if 'email' not in body or not body['email']:
                raise serializers.ValidationError("Email is required and cannot be empty.")
            
            if 'password' not in body or not body['password'] or len(body['password']) < 8:
                raise serializers.ValidationError("Password is required and cannot be empty.")
            
            if 'name' not in body or not body['name']:
                raise serializers.ValidationError("Name is required and cannot be empty.")
            
            if 'ph_no' not in body or not body['ph_no']:
                raise serializers.ValidationError("Phone number is required and cannot be empty.")
            # Create an Profile object
            with transaction.atomic():
                user_obj = User(name=body['name'],email=body['email'],ph_no=body['ph_no'],role='teacher',email_verified=True)
                user_obj.set_password(body['password'])
                user_obj.save()
                # Create an teacher object
                teacher_obj = Teacher.objects.create(profile=user_obj,branch=branch_obj)
            teachers_serialized = TeacherSerializer(teacher_obj,many=False)
            data = {'teacher':teachers_serialized.data}
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_subjects_to_teacher(request):
    '''
    # Add Subjects to Teacher

    Updates the list of subjects assigned to a teacher.

    - Method: `PUT`
    - Authentication: Required (`IsAuthenticated`)

    ### Request

    - Endpoint: `/api/add_subjects_to_teacher`
    - Headers:
    - `Authorization`: Bearer Token

    #### Input Parameters

    1. `teacher_id` (integer, required): Unique identifier of the teacher.
    2. `selected_subjects` (array of strings, required): Array of subject slugs to be assigned to the teacher.

    #### Sample Request Body

    ```json
    {
        "teacher_id": 1,
        "selected_subjects": ["551162_1700243634", "223792_1700243634", "173253_1700242491"]
    }
    ```

    ### Response

    #### Successful Response (Status Code: 200)

    ```json
    {
        "teacher": {
            "profile": {
                "name": "Kishan Noorani",
                "email": "kishan@gmail.com",
                "ph_no": "9925717005"
            },
            "subjects": [
                {
                    "subject_name": "Software Engineering",
                    "code": 3150711,
                    "credit": 5,
                    "slug": "173253_1700242491"
                },
                {
                    "subject_name": "Analysis And Design Of Algorithms",
                    "code": 3150703,
                    "credit": 5,
                    "slug": "223792_1700243634"
                },
                {
                    "subject_name": "Computer Networks",
                    "code": 3150710,
                    "credit": 5,
                    "slug": "551162_1700243634"
                }
            ]
        }
    }
    ```

    #### Error Responses

    - Status Code: 401
    ```json
    {"data": "You're not allowed to perform this action"}
    ```

    - Status Code: 500
    ```json
    {"data": "Error message"}
    ```
    '''
    try:
        if request.user.role == 'admin':            
            body = request.data
            if 'teacher_id' not in body or not body['teacher_id']:
                raise serializers.ValidationError("Please pass unique id of the teacher")
            
            if 'selected_subjects' not in body or not body['selected_subjects'] or len(body['selected_subjects']) == 0:
                raise serializers.ValidationError("Pleae pass a valid subjects array")

            teacher_obj = Teacher.objects.get(id=body['teacher_id'])                        
            with transaction.atomic():
                for i in body['selected_subjects']:                    
                    subject_obj = Subject.objects.get(slug=i)                    
                    teacher_obj.subjects.add(subject_obj)
            teachers_serialized = TeacherSerializer(teacher_obj,many=False)
            data = {'teacher':teachers_serialized.data}
            return JsonResponse(data,status=200)
        else:
            data = {"data":"You're not allowed to perform this action"}
            return JsonResponse(data,status=401)
    except Exception as e:
        data = {"data":str(e)}
        return JsonResponse(data,status=500)
    
