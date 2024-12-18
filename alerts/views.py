from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from .models import TradingAlert
import json
import logging
from utils.security import generate_access_token, encrypt_payload
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib import messages

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def tradingview_webhook(request):
    try:
        data = json.loads(request.body)
        strategy = data.get('strategy', {})
        
        # Create new alert
        alert = TradingAlert.objects.create(
            position_size=strategy.get('position_size', 0),
            order_action=strategy.get('order_action', ''),
            order_contracts=strategy.get('order_contracts', 0),
            order_price=strategy.get('order_price', 0),
            order_id=strategy.get('order_id', ''),
            market_position=strategy.get('market_position', ''),
            market_position_size=strategy.get('market_position_size', 0),
            prev_market_position=strategy.get('prev_market_position', ''),
            prev_market_position_size=strategy.get('prev_market_position_size', 0)
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Alert received',
            'order_id': alert.order_id
        })
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON data received")
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_latest_alert(request):
    try:
        latest_alert = TradingAlert.objects.first()
        if (latest_alert):
            return JsonResponse({
                'status': 'success',
                'data': {
                    'position_size': latest_alert.position_size,
                    'order_action': latest_alert.order_action,
                    'order_contracts': latest_alert.order_contracts,
                    'order_price': latest_alert.order_price,
                    'order_id': latest_alert.order_id,
                    'market_position': latest_alert.market_position,
                    'market_position_size': latest_alert.market_position_size,
                    'timestamp': latest_alert.timestamp.isoformat()
                }
            })
        return JsonResponse({
            'status': 'success',
            'data': None
        })
    except Exception as e:
        logger.error(f"Error fetching latest alert: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

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
