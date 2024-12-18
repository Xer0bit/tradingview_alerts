import os
import django
from utils.ip_config import get_public_ip, get_available_port

def main():
    public_ip = get_public_ip()
    port = get_available_port()
    
    print(f"Server will start at: http://{public_ip}:{port}")
    print(f"You can use this URL for your TradingView webhooks")
    print(f"Webhook endpoint: http://{public_ip}:{port}/alerts/webhook/?jsonrequest=true")
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradingview_alerts.settings')
    django.setup()
    
    os.system(f"python manage.py runserver 0.0.0.0:{port}")

if __name__ == "__main__":
    main()
