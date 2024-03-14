import json

from django.http import JsonResponse

from Appointment_System_API.models import Customer, Department, Employee, Appointment


def create_customer(request):
    try:
        data = json.loads(request.body)

        customer = Customer.objects.create(
            fullname=data.get('fullname'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        customer.save()

        return JsonResponse({"message": "Customer created successfully"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)


def create_department(request):
    try:
        data = json.loads(request.body)

        department = Department.objects.create(
            fullname=data.get('fullname'),
            address=data.get('address')
        )
        department.save()

        return JsonResponse({"message": "Department created successfully"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)


def create_employee(request):
    try:
        data = json.loads(request.body)

        department = Department.objects.get(id=data.get('departmentId'))

        employee = Employee.objects.create(
            fullname=data.get('fullname'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            department=department
        )
        employee.save()

        return JsonResponse({"message": "Employee created successfully"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
    except Department.DoesNotExist:
        return JsonResponse({"message": "Department was not found"}, status=400)


def create_appointment(request):
    try:
        data = json.loads(request.body)

        employee = Employee.objects.get(id=data.get('employeeId'))
        customer = Customer.objects.get(id=data.get('customerId'))

        appointment = Appointment.objects.create(
            date=data.get('date'),
            start=data.get('start'),
            end=data.get('end'),
            employee=employee,
            customer=customer
        )
        appointment.save()

        return JsonResponse({"message": "Appointment created successfully"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)
    except Employee.DoesNotExist:
        return JsonResponse({"message": "Employee was not found"}, status=400)
    except Customer.DoesNotExist:
        return JsonResponse({"message": "Customer was not found"}, status=400)
