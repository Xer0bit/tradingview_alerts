from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST", "GET"])
def webhook_alert(request):
    if request.method == "GET":
        json_request = request.GET.get('jsonrequest', 'false').lower() == 'true'
        return JsonResponse({
            'status': 'ready',
            'endpoint': '/alerts/webhook/',
            'jsonrequest': json_request
        })
        
    try:
        data = json.loads(request.body)
        print(f"Received webhook alert: {data}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Webhook alert received',
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
