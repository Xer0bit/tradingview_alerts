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
    base_url = "http://139.59.121.41:80"
    webhook_url = f"{base_url}/alerts/webhook/"
    
    headers = {
        'Content-Type': 'text/plain',
        'Accept': 'text/plain',
        'Host': '139.59.121.41',
        'Origin': 'http://139.59.121.41',
        'Referer': 'http://139.59.121.41'
    }

    test_cases = [
        "Alert message: BUY BTCUSD @ 50000",
        "Alert message: SELL ETHUSD @ 2500",
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
