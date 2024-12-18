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
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    test_cases = [
        {
            "strategy": {
                "position_size": 100,
                "order_action": "buy",
                "order_contracts": 1,
                "order_price": 50000,
                "order_id": "test_1",
                "market_position": "long",
                "market_position_size": 1,
                "prev_market_position": "flat",
                "prev_market_position_size": 0
            }
        }
    ]
    
    # Test each payload
    for i, payload in enumerate(test_cases, 1):
        try:
            logger.info(f"\nTest Case {i} - Sending payload: {json.dumps(payload, indent=2)}")
            response = requests.post(webhook_url, json=payload, headers=headers)
            
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
