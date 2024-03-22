import json

from django.http import JsonResponse
from django.views import View

from api.auth.permissions import has_permission
from api.departments.models import Department
from api.departments.serializers import DepartmentSerializer
from api.response import Response


class DepartmentView(View):
    @staticmethod
    @has_permission('view_department')
    def get(request, id):
        try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department)
            response = Response(model=serializer.data, message="Department was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Department.DoesNotExist:
            response = Response(message="Department was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_department')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = DepartmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Department was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_department')
    def put(request, id):
        try:
            data = json.loads(request.body)

            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(instance=department, data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Department was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Department.DoesNotExist:
            response = Response(message="Department was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_department')
    def delete(request, id):
        try:
            department = Department.objects.get(id=id)
            department.delete()
            response = Response(message="Department was deleted successfully")
            return JsonResponse(response.__dict__, status=200)
        except Department.DoesNotExist:
            response = Response(message="Department was not found")
            return JsonResponse(response.__dict__, status=400)


class DepartmentListView(View):
    @staticmethod
    @has_permission('view_department')
    def get(request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        response = Response(model=serializer.data,
                            message="List of departments was retrieved successfully")
        return JsonResponse(response.__dict__, status=200)
