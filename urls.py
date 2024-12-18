from django.urls import path
from alerts.server import webhook_alert

urlpatterns = [
    path('alerts/webhook/', webhook_alert, name='webhook_alert'),
]
