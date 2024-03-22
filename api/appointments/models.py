from django.db import models


class Appointment(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('view_other_appointment', 'Can view other appointment')
        ]
