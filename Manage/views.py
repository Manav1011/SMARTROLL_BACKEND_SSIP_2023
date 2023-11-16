from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from StakeHolders.models import Admin
from .serializers import BatchSerializer,SemesterSerializer
from rest_framework.views import APIView
from Manage.models import Batch
# Create your views here.

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
    if request.user.role == 'admin':
        admin_obj = Admin.objects.get(profile=request.user)
        batches = admin_obj.branch.batches        
        if batches.exists():            
            batch_serialized_obj = BatchSerializer(batches,many=True)
            data = {'data':batch_serialized_obj.data}
            return JsonResponse(data,status=200)
        else:
            data = {"data":"Currently there are no active batches"}
            return JsonResponse(data,status=204)
    else:
        data = {"data":"You're not allowed to perform this action"}
        return JsonResponse(data,status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_batches(request):
    '''    
    ### Add Batches

    **Description:** Add a new batch to admin's branch.

    **Endpoint:** `/add_batches`

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

    - `batch_id` (integer, required): ID of the batch for which semesters are to be retrieved.

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
            body = request.data
            admin_obj = Admin.objects.get(profile=request.user)
            if body.get('batch_id') and int(body['batch_id']) > 0:
                batch_obj = admin_obj.branch.batches.get(id=body['batch_id'])        
                if batch_obj:
                    semesters = batch_obj.semesters
                    if semesters.exists():
                        semesters_serialized = SemesterSerializer(semesters,many=True)
                        data = {'data':semesters_serialized.data}
                        return JsonResponse(data,status=200)
                    else:
                        data = {"data":"Currently there are no active semesters in this batch"}
                        return JsonResponse(data,status=204)               
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