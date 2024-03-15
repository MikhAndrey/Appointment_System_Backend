from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)


class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)


class Department(models.Model):
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Appointment(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)