from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TradingViewAlert
import logging
import json

logger = logging.getLogger(__name__)

@csrf_exempt
def tradingview_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Store the alert
            alert = TradingViewAlert.objects.create(strategy=data)
            
            # Log the received alert
            logger.info(f"Received alert: {data}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Alert stored successfully',
                'alert_id': alert.id
            })
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Error processing alert: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Internal server error'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method is allowed'
    }, status=405)

def get_latest_alert(request):
    try:
        latest_alert = TradingViewAlert.objects.first()
        if latest_alert:
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': latest_alert.id,
                    'strategy': latest_alert.strategy,
                    'received_at': latest_alert.received_at.isoformat(),
                }
            })
        return JsonResponse({
            'status': 'error',
            'message': 'No alerts found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error fetching latest alert: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)
