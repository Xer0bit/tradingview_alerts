import requests
import json
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_webhook():
    base_url = "http://localhost:8000"
    webhook_url = f"{base_url}/alerts/webhook/"
    
    headers = {
        'Content-Type': 'text/plain',
        'Accept': 'text/plain',
        'Host': 'localhost:8000'
    }

    test_cases = [
        "XAUUSD-LONG|ENTRY:2626.39|SL:2573.86|TP1:2678.92|TP2:2731.45|TP3:2783.98|TP4:2836.5|TP5:2889.03",
        "EURUSD-SHORT|ENTRY:1.0850|SL:1.0900|TP1:1.0800|TP2:1.0750"
    ]
    
    # Test each payload
    for i, message in enumerate(test_cases, 1):
        try:
            logger.info(f"\nTest Case {i} - Sending message: {message}")
            response = requests.post(webhook_url, data=message, headers=headers)
            
            logger.info("\nResponse Details:")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            logger.info(f"Response Body: {response.text}")
            
            # Test getting latest alert
            time.sleep(1)  # Wait for alert to be processed
            latest_alert_response = requests.get(f"{base_url}/alerts/latest/")
            logger.info("\nLatest Alert Response:")
            logger.info(f"Status Code: {latest_alert_response.status_code}")
            logger.info(f"Response Body: {latest_alert_response.text}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            logger.info("-" * 50)

if __name__ == "__main__":
    logger.info("Starting webhook tests...")
    test_webhook()
    logger.info("Completed webhook tests")
