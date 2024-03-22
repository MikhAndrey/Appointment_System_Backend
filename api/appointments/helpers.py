from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_appointment_notification(message_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'appointment_notifications',
        {
            'type': message_type,
            'data': data
        }
    )
