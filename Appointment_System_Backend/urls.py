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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from api import views
from api.appointments import views as appointment_views
from api.employees import views as employee_views
from api.customers import views as customer_views
from api.departments import views as department_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers', customer_views.CustomerView.as_view(http_method_names=['post'])),
    path('customers/<int:id>', customer_views.CustomerView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('customers/list', customer_views.CustomerListView.as_view(http_method_names=['get'])),
    path('customers/shortList', customer_views.CustomerShortListView.as_view(http_method_names=['get'])),
    path('departments', department_views.DepartmentView.as_view(http_method_names=['post'])),
    path('departments/<int:id>', department_views.DepartmentView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('departments/list', department_views.DepartmentListView.as_view(http_method_names=['get'])),
    path('appointments', appointment_views.AppointmentView.as_view(http_method_names=['post'])),
    path('appointments/<int:id>', appointment_views.AppointmentView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('appointments/list', appointment_views.AppointmentListView.as_view(http_method_names=['get'])),
    path('employees', employee_views.EmployeeView.as_view(http_method_names=['post'])),
    path('employees/<int:id>', employee_views.EmployeeView.as_view(http_method_names=['put', 'delete', 'get'])),
    path('employees/list', employee_views.EmployeeListView.as_view(http_method_names=['get'])),
    path('employees/shortList', employee_views.EmployeeShortListView.as_view(http_method_names=['get'])),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/remove', TokenBlacklistView.as_view(), name='token_refresh'),
    path('groups/list', views.GroupListView.as_view(http_method_names=['get'])),
]
