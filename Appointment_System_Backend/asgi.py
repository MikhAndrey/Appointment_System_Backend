"""
ASGI config for Appointment_System_Backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from api.websockets.consumers import AppointmentConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Appointment_System_Backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': URLRouter([
            path('ws/appointments/', AppointmentConsumer.as_asgi()),
        ]),
    }
)
