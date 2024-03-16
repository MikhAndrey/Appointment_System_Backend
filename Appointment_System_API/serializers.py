from rest_framework import serializers

from Appointment_System_API.models import Customer, Department, Employee, Appointment


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    employeeId = serializers.PrimaryKeyRelatedField(source='employee', queryset=Employee.objects.all())
    employeeId.default_error_messages['does_not_exist'] = 'Employee was not found'

    customerId = serializers.PrimaryKeyRelatedField(source='customer', queryset=Customer.objects.all())
    employeeId.default_error_messages['does_not_exist'] = 'Customer was not found'

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'start', 'end', 'employeeId', 'customerId']
