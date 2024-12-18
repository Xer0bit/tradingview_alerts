from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='admin_logout'),
    path('', views.test_panel, name='test_panel'),
    path('generate-token/', views.generate_panel_token, name='generate_token'),
    path('webhook/', views.tradingview_webhook, name='webhook'),
    path('latest/', views.get_latest_alert, name='latest_alert'),
    path('test/', views.test_panel, name='test_panel'),
]

