from django.shortcuts import render
from.models import *
# Create your views here.

import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
import random
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser








def generate_password(employee_code):
    rendom_number = random.randint(1000,9999)
    return f"{employee_code}@{rendom_number}"





def create_employee_from_data(data):
    try:
        username = data['username']
        employee_code = data['employee_code']
        fullname = data['fullname']
        role_names = data['role'].split(',') if isinstance(data['role'], str) else data['role']  # Handle multiple roles
        warehouse_list = data['warehouse'].split(',') if isinstance(data['warehouse'], str) else data['warehouse']
        email = data['email']
        mobile = data['mobile']
        city_name = data['city']
        inv_owners = data['inv_owner'].split(',') if isinstance(data['inv_owner'], str) else data['inv_owner']  # Handle multiple inv_owners

        password = generate_password(employee_code)
        user = User.objects.create_user(username=username, password=password, email=email)

        # Fetch related objects
        # roles = Role.objects.filter(role_name__in=role_names)
        # warehouses = Warehouse.objects.filter(name__in=warehouse_list)
        # city = City.objects.get(city_name=city_name)
        # inv_owners = InventoryOwner.objects.filter(name__in=inv_owners)

        # Create employee
        employee = EmployeeMaster.objects.create(
            user=user,
            employee_code=employee_code,
            fullname=fullname,
            email=email,
            mobile=mobile,
            city=city_name,
            role = role_names,
            warehouse = warehouse_list,
            inv_owner = inv_owners
        )

        # # Set many-to-many relationships
        # employee.warehouse.set(warehouses)
        # employee.role.set(roles)
        # employee.inv_owner.set(inv_owners)

        return username, password

    except Exception as e:
        # Optionally log the error or handle it as needed
        raise ValueError(f"Failed to create employee: {str(e)}")  # Raise a descriptive error


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser,JSONParser])
def create_employee(request):
    print("create_employee view has been called")
    print(f"Files in request: {request.FILES.keys()}")
    
    if 'file' in request.FILES:
        excel_file = request.FILES['file']
        print(f"Received file: {excel_file}")

        try:
            df = pd.read_excel(excel_file)  # Read the Excel file into a DataFrame
            print(df)
        except Exception as e:
            return Response({
                'error': str(e),
                'message': 'Failed to read the Excel file.'
            }, status=status.HTTP_400_BAD_REQUEST)

        employees_created = []
        for index, row in df.iterrows():
            try:
                print(f"Processing row {index}: {row}")
                username, password = create_employee_from_data(row)  # Ensure this function handles the DataFrame row correctly
                employees_created.append({'username': username, 'password': password})  # Store both username and password
            except Exception as e:
                return Response({
                    'error': str(e),
                    'message': f'Error while creating employee at row {index}.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'employees_created': employees_created,
            'message': 'Employees created successfully.'
        }, status=status.HTTP_201_CREATED)

    else:
        # If no Excel file is present, use the normal creation method
        data = request.data
        try:
            username, password = create_employee_from_data(data)
            return Response([{
                'username': username,
                'password': password,
                'message': 'Employee created successfully.'
            }], status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response([{
                'error': str(e),
                'message': 'Error while creating employee.'
            }], status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def import_excel(request):
    print("create_employee view has been called")
    
    if 'file' not in request.FILES:
        return Response({
            "status": "error",
            "message": "No file provided in the request."
        }, status=400)
    
    excel_file = request.FILES['file']
    print(f"Received file: {excel_file.name}")

    try:
        df = pd.read_excel(excel_file)
        print(df)  # Print the DataFrame to the console

        # Add logic here to process the DataFrame and create employees, if needed.

        return Response({
            "status": "success",
            "message": "File processed successfully."
        }, status=200)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=500)