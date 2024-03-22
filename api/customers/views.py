import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from api.auth.permissions import has_permission
from api.customers.models import Customer
from api.customers.serializers import CustomerSerializer, CustomerShortSerializer
from api.response import Response, PageResponse


class CustomerView(View):
    @staticmethod
    @has_permission('view_customer')
    def get(request, id):
        try:
            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(customer)
            response = Response(model=serializer.data, message="Customer was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Customer.DoesNotExist:
            response = Response(message="Customer was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_customer')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Customer was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_customer')
    def put(request, id):
        try:
            data = json.loads(request.body)

            customer = Customer.objects.get(id=id)
            serializer = CustomerSerializer(instance=customer, data=data)
            if serializer.is_valid():
                serializer.save()
                response = Response(model=serializer.data, message="Customer was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Customer.DoesNotExist:
            response = Response(message="Customer was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_customer')
    def delete(request, id):
        try:
            customer = Customer.objects.get(id=id)
            customer.delete()
            response = Response(message="Customer was deleted successfully")
            return JsonResponse(response.__dict__, status=200)
        except Customer.DoesNotExist:
            response = Response(message="Customer was not found")
            return JsonResponse(response.__dict__, status=400)


class CustomerListView(View):
    @staticmethod
    @has_permission('view_customer')
    def get(request):
        queryset = Customer.objects.all().order_by('id')
        page_number = request.GET.get('pageNumber')
        per_page = request.GET.get('pageSize')
        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

        serializer = CustomerSerializer(page_obj.object_list, many=True)
        response = PageResponse(
            model=serializer.data,
            message="Page of customers was retrieved successfully",
            page_obj=page_obj,
            paginator=paginator
        )
        return JsonResponse(response.__dict__(), status=200)


class CustomerShortListView(View):
    @staticmethod
    def get(request):
        queryset = Customer.objects.all()
        serializer = CustomerShortSerializer(queryset, many=True)
        response = Response(model=serializer.data)
        return JsonResponse(response.__dict__, status=200)
