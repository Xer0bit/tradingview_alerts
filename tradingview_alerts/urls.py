"""
URL configuration for tradingview_alerts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from alerts.views import admin_login, test_panel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alerts/', include('alerts.urls')),
    path('alerts/admin-login/', admin_login, name='admin_login'),
    path('alerts/test-panel/', test_panel, name='test_panel'),
]


