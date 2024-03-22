import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View

from api.appointments.helpers import send_appointment_notification
from api.appointments.models import Appointment
from api.appointments.serializers import AppointmentGetSerializer, AppointmentSerializer
from api.auth.permissions import has_permission, user_has_permission
from api.response import PageResponse, Response


class AppointmentView(View):
    @staticmethod
    @has_permission('view_own_appointment')
    def get(request, id):
        try:
            if user_has_permission(request.user, 'view_other_appointment'):
                appointment = Appointment.objects.get(id=id)
            else:
                appointment = Appointment.objects.get(id=id, employee=request.user.employee)
            serializer = AppointmentGetSerializer(appointment)
            response = Response(model=serializer.data, message="Appointment was retrieved successfully")
            return JsonResponse(response.__dict__, status=200)
        except Appointment.DoesNotExist:
            response = Response(message="Appointment was not found")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('add_appointment')
    def post(request):
        try:
            data = json.loads(request.body)
            serializer = AppointmentSerializer(data=data)
            if serializer.is_valid():
                appointment = serializer.save()
                serializer = AppointmentGetSerializer(appointment)
                send_appointment_notification('appointment.create', serializer.data)
                response = Response(model=serializer.data, message="Appointment was created successfully")
                return JsonResponse(response.__dict__, status=201)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('change_appointment')
    def put(request, id):
        try:
            data = json.loads(request.body)

            appointment = Appointment.objects.get(id=id)
            serializer = AppointmentSerializer(instance=appointment, data=data)
            if serializer.is_valid():
                appointment = serializer.save()
                serializer = AppointmentGetSerializer(appointment)
                send_appointment_notification('appointment.update', serializer.data)
                response = Response(model=serializer.data, message="Appointment was updated successfully")
                return JsonResponse(response.__dict__, status=200)
            else:
                response = Response(errors=serializer.errors)
                return JsonResponse(response.__dict__, status=400)
        except Appointment.DoesNotExist:
            response = Response(message="Appointment was not found")
            return JsonResponse(response.__dict__, status=400)
        except json.JSONDecodeError:
            response = Response(message="Invalid JSON")
            return JsonResponse(response.__dict__, status=400)

    @staticmethod
    @has_permission('delete_appointment')
    def delete(request, id):
        try:
            appointment = Appointment.objects.get(id=id)
            appointment.delete()
            send_appointment_notification('appointment.delete', id)
            response = Response(message="Appointment was deleted successfully")
            return JsonResponse(response.__dict__, status=200)
        except Appointment.DoesNotExist:
            response = Response(message="Appointment was not found")
            return JsonResponse(response.__dict__, status=400)


class AppointmentListView(View):
    @staticmethod
    @has_permission('view_appointment')
    def get(request):
        if user_has_permission(request.user, 'view_other_appointment'):
            queryset = Appointment.objects.all().order_by('id')
        else:
            queryset = Appointment.objects.filter(employee=request.user.employee).order_by('id')
        page_number = request.GET.get('pageNumber')
        per_page = request.GET.get('pageSize')
        paginator = Paginator(queryset, per_page)

        try:
            page_obj = paginator.page(page_number)
        except:
            page_obj = paginator.page(1)

        serializer = AppointmentGetSerializer(page_obj.object_list, many=True)
        response = PageResponse(
            model=serializer.data,
            message="Page of appointments was retrieved successfully",
            page_obj=page_obj,
            paginator=paginator
        )
        return JsonResponse(response.__dict__(), status=200)
