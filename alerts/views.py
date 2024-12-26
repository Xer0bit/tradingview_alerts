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

def parse_alert_text(text):
    """Parse TradingView alert text into structured JSON format"""
    try:
        # Check if text is empty or invalid
        if not text or '|' not in text or '-' not in text.split('|')[0]:
            return json.dumps({
                "error": "Invalid alert format",
                "raw_text": text
            })

        # Split by pipe character
        parts = text.split('|')
        
        # Parse symbol and direction from first part
        try:
            symbol_direction = parts[0].split('-')
            symbol = symbol_direction[0]
            direction = symbol_direction[1]
        except IndexError:
            return json.dumps({
                "error": "Invalid symbol-direction format",
                "raw_text": text
            })
        
        # Initialize data dictionary with a cleaner structure
        data = {
            "symbol": symbol,
            "direction": direction,
            "entry": None,
            "stopLoss": None,
            "takeProfits": {},
            "raw_text": text  # Store original text for reference
        }
        
        # Parse remaining parts
        for part in parts[1:]:
            try:
                key, value = part.split(':')
                price = float(value)
                
                # Map to specific fields
                if key == 'ENTRY':
                    data['entry'] = price
                elif key == 'SL':
                    data['stopLoss'] = price
                elif key.startswith('TP'):
                    data['takeProfits'][key] = price
            except (ValueError, IndexError):
                continue  # Skip invalid parts
        
        # Sort take profits by TP number
        data['takeProfits'] = dict(sorted(data['takeProfits'].items()))
        
        # Calculate risk and rewards only if we have valid entry and stop loss
        if data['entry'] is not None and data['stopLoss'] is not None:
            data['riskPips'] = abs(data['entry'] - data['stopLoss'])
            data['rewards'] = {
                tp: abs(price - data['entry']) / data['riskPips']
                for tp, price in data['takeProfits'].items()
            }
        
        return json.dumps(data, indent=2)
        
    except Exception as e:
        logger.error(f"Error parsing alert text: {str(e)}")
        return json.dumps({
            "error": "Failed to parse alert",
            "raw_text": text
        })

@csrf_exempt
def tradingview_webhook(request):
    if request.method == 'POST':
        try:
            # Try to parse as JSON first
            try:
                data = json.loads(request.body.decode('utf-8'))
                alert_text = json.dumps(data)
            except json.JSONDecodeError:
                # If not JSON, try to parse the format
                raw_text = request.body.decode('utf-8')
                alert_text = parse_alert_text(raw_text)
            
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
        # Get last 5 alerts instead of just one
        latest_alerts = TradingViewAlert.objects.all()[:5]
        alerts_data = []
        
        for alert in latest_alerts:
            try:
                # First try to parse as JSON
                try:
                    stored_data = json.loads(alert.text_data)
                except json.JSONDecodeError:
                    # If not valid JSON, parse as alert text
                    stored_data = json.loads(parse_alert_text(alert.text_data))
                
                alerts_data.append({
                    'timestamp': alert.received_at.isoformat(),
                    'data': stored_data
                })
            except Exception as e:
                # If all parsing fails, include raw text
                alerts_data.append({
                    'timestamp': alert.received_at.isoformat(),
                    'data': {
                        'error': 'Failed to parse alert',
                        'raw_text': alert.text_data
                    }
                })
        
        return JsonResponse({
            'alerts': alerts_data,
            'count': len(alerts_data)
        })
        
    except Exception as e:
        logger.error(f"Error fetching latest alerts: {str(e)}")
        return JsonResponse({
            'error': str(e),
            'alerts': []
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
