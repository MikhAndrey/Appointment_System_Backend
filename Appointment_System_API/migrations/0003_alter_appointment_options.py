# Generated by Django 5.0.3 on 2024-03-16 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_System_API', '0002_remove_employee_email_remove_employee_fullname_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'permissions': [('view_own_appointment', 'Can view own appointment'), ('view_other_appointment', 'Can view other appointment')]},
        ),
    ]