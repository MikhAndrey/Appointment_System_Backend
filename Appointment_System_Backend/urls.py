"""
URL configuration for Appointment_System_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Appointment_System_API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers', views.CustomerView.as_view(http_method_names=['post'])),
    path('customers/<int:id>', views.CustomerView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('customers/list', views.CustomerListView.as_view(http_method_names=['get'])),
    path('departments', views.DepartmentView.as_view(http_method_names=['post'])),
    path('departments/<int:id>', views.DepartmentView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('departments/list', views.DepartmentListView.as_view(http_method_names=['get'])),
    path('appointments', views.AppointmentView.as_view(http_method_names=['post'])),
    path('appointments/<int:id>', views.AppointmentView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('appointments/list', views.AppointmentListView.as_view(http_method_names=['get'])),
    path('employees', views.EmployeeView.as_view(http_method_names=['post'])),
    path('employees/<int:id>', views.EmployeeView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('employees/list', views.EmployeeListView.as_view(http_method_names=['get'])),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
