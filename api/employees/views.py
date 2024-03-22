import json

from django.db import transaction
from django.http import JsonResponse
from django.views import View
from rest_framework import serializers

from api.auth.permissions import has_permission
from api.employees.models import Employee
from api.employees.serializers import EmployeeSerializer, EmployeeGetSerializer, EmployeeShortSerializer
from api.response import Response


class EmployeeView(View):
    @staticmethod
    @has_permission('view_employee')
    def get(request, id):
        try:
            employee = Employee.objects.get(id=id)
            serializer = EmployeeGetSerializer(employee)
            response = Response(model=serializer.data, message="Employee was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Employee.DoesNotExist:
            response = Response(message="Employee was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_employee')
    @transaction.atomic
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                employee = serializer.save()
                serializer = EmployeeGetSerializer(employee)
                response = Response(model=serializer.data, message="Employee was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)
        except serializers.ValidationError as e:
            response = Response(errors=e.detail)
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_employee')
    @transaction.atomic
    def put(request, id):
        try:
            data = json.loads(request.body)

            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(instance=employee, data=data)
            if serializer.is_valid():
                employee = serializer.save()
                serializer = EmployeeGetSerializer(employee)
                response = Response(model=serializer.data, message="Employee was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Employee.DoesNotExist:
            response = Response(message="Employee was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)
        except serializers.ValidationError as e:
            response = Response(errors=e.detail)
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_employee')
    def delete(request, id):
        try:
            employee = Employee.objects.get(id=id)
            employee.delete()
            employee.user.delete()
            response = Response(message="Employee was deleted successfully")
            return JsonResponse(response.__dict__, status=200)
        except Employee.DoesNotExist:
            response = Response(message="Employee was not found")
            return JsonResponse(response.__dict__, status=400)


class EmployeeListView(View):
    @staticmethod
    @has_permission('view_employee')
    def get(request):
        queryset = Employee.objects.all()
        serializer = EmployeeGetSerializer(queryset, many=True)
        response = Response(model=serializer.data,
                            message="List of employees was retrieved successfully")
        return JsonResponse(response.__dict__, status=200)


class EmployeeShortListView(View):
    @staticmethod
    def get(request):
        queryset = Employee.objects.all()
        serializer = EmployeeShortSerializer(queryset, many=True)
        response = Response(model=serializer.data)
        return JsonResponse(response.__dict__, status=200)
