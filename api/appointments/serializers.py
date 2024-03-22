from rest_framework import serializers

from api.appointments.models import Appointment
from api.customers.models import Customer
from api.employees.models import Employee


class AppointmentGetSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'start', 'end', 'employee', 'customer']

    def get_employee(self, obj: Appointment):
        return {
            "id": obj.employee.id,
            "fullname": obj.employee.user.username
        }

    def get_customer(self, obj: Appointment):
        return {
            "id": obj.customer.id,
            "fullname": obj.customer.fullname
        }


class AppointmentSerializer(serializers.ModelSerializer):
    employeeId = serializers.PrimaryKeyRelatedField(source='employee', queryset=Employee.objects.all())
    employeeId.default_error_messages['does_not_exist'] = 'Employee was not found'

    customerId = serializers.PrimaryKeyRelatedField(source='customer', queryset=Customer.objects.all())
    employeeId.default_error_messages['does_not_exist'] = 'Customer was not found'

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'start', 'end', 'employeeId', 'customerId']
