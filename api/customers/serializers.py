from rest_framework import serializers

from api.customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'fullname']
