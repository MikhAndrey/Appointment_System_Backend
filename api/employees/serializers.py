from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from rest_framework import serializers

from api.departments.models import Department
from api.employees.models import Employee
from Appointment_System_Backend.settings import EMAIL_HOST_USER


class EmployeeGetSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    email = serializers.EmailField(source='user.email')
    fullname = serializers.CharField(source='user.username')
    roles = serializers.SerializerMethodField('get_employee_roles')

    def get_employee_roles(self, obj: Employee):
        return [group.name for group in obj.user.groups.all()]

    class Meta:
        model = Employee
        fields = ['id', 'fullname', 'email', 'phone', 'address', 'department', 'roles']

    def get_department(self, obj: Employee):
        return {
            "id": obj.department.id,
            "fullname": obj.department.fullname
        }


class EmployeeSerializer(serializers.ModelSerializer):
    departmentId = serializers.PrimaryKeyRelatedField(source='department', queryset=Department.objects.all())
    departmentId.default_error_messages['does_not_exist'] = 'Department was not found'

    email = serializers.EmailField()
    fullname = serializers.CharField()
    roles = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Employee
        fields = ['email', 'fullname', 'roles', 'phone', 'address', 'departmentId']

    def create(self, validated_data):
        password = User.objects.make_random_password()
        hashed_password = make_password(password)

        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['fullname'],
            password=hashed_password
        )

        subject = 'Your Generated Password'
        message = f'Your generated password is: {password}'
        sender = EMAIL_HOST_USER
        recipient = user.email
        send_mail(subject, message, sender, [recipient])

        try:
            for role in validated_data['roles']:
                group = Group.objects.get(name=role)
                group.user_set.add(user)
        except Group.DoesNotExist:
            raise serializers.ValidationError('Group does not exist')

        employee = Employee.objects.create(
            user=user,
            phone=validated_data['phone'],
            address=validated_data['address'],
            department=validated_data['department']
        )

        return employee

    def update(self, instance: Employee, validated_data):
        instance.user.email = validated_data['email']
        instance.user.username = validated_data['fullname']
        instance.phone = validated_data['phone']
        instance.address = validated_data['address']
        instance.department = validated_data['department']

        instance.user.groups.clear()
        try:
            for role in validated_data['roles']:
                group = Group.objects.get(name=role)
                group.user_set.add(instance.user)
        except Group.DoesNotExist:
            raise serializers.ValidationError('Group does not exist')

        instance.save()
        instance.user.save()
        return instance


class EmployeeShortSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField('get_employee_fullname')

    class Meta:
        model = Employee
        fields = ['id', 'fullname']

    def get_employee_fullname(self, obj: Employee):
        return obj.user.username
