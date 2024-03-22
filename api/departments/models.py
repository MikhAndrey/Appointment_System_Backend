from django.db import models


class Department(models.Model):
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
