from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.tradingview_webhook, name='tradingview_webhook'),
    path('latest/', views.get_latest_alert, name='get_latest_alert'),
]
