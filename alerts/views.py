from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from .models import TradingViewAlert
import json
import logging
from utils.security import generate_access_token, encrypt_payload
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages

logger = logging.getLogger(__name__)

@csrf_exempt
def tradingview_webhook(request):
    if request.method == 'POST':
        try:
            # Try to parse as JSON first
            try:
                data = json.loads(request.body.decode('utf-8'))
                alert_text = json.dumps(data)
            except json.JSONDecodeError:
                # If not JSON, treat as plain text
                alert_text = request.body.decode('utf-8')
            
            # Save the alert
            alert = TradingViewAlert.objects.create(
                text_data=alert_text
            )
            
            return HttpResponse("Alert received successfully", status=200)
            
        except Exception as e:
            logger.error(f"Error processing alert: {str(e)}")
            return HttpResponse("Error processing alert", status=500)
    
    return HttpResponse("Method not allowed", status=405)

def get_latest_alert(request):
    try:
        latest_alert = TradingViewAlert.objects.first()
        if latest_alert:
            return JsonResponse({
                'id': latest_alert.id,
                'text': latest_alert.text_data,
                'received_at': latest_alert.received_at.isoformat()
            })
        return JsonResponse({'message': 'No alerts found'})
    except Exception as e:
        logger.error(f"Error fetching latest alert: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def generate_panel_token(request):
    token = generate_access_token()
    return JsonResponse({
        'status': 'success',
        'token': token,
        'expires_in': 86400  # 24 hours
    })

@login_required
@user_passes_test(is_admin)
def test_panel(request):
    # Generate encrypted test payload
    test_payload = {
        "strategy": {
            "position_size": 100,
            "order_action": "buy",
            "order_contracts": 1,
            "order_price": 50000,
            "order_id": "secure_test_1",
            "market_position": "long",
            "market_position_size": 1,
            "prev_market_position": "flat",
            "prev_market_position_size": 0
        }
    }
    encrypted_payload = encrypt_payload(str(test_payload))
    return render(request, 'alerts/test_panel.html', {
        'encrypted_payload': encrypted_payload
    })

def test_panel(request):
    """
    Simple view to render the test panel interface
    """
    return render(request, 'alerts/test_panel.html')

# Add new login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('test_panel')
        else:
            messages.error(request, 'Invalid credentials or not an admin')
    return render(request, 'alerts/admin_login.html')
