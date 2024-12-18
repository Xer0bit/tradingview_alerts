import requests
import json
import logging
from utils.ip_config import get_public_ip, get_available_port

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_webhook():
    # Get the same IP and port as the server uses
    ip = get_public_ip()
    port = get_available_port()
    
    base_url = f"http:///192.168.1.54:8000"
    webhook_url = f"{base_url}/alerts/webhook/"  # Updated URL path
    
    # Example test payloads
    test_cases = [
        {
            "strategy": {
                "position_size": 100,
                "order_action": "buy",
                "order_contracts": 1,
                "order_price": 50000,
                "order_id": "test_order_1",
                "market_position": "long",
                "market_position_size": 1,
                "prev_market_position": "flat",
                "prev_market_position_size": 0
            }
        },
        {
            "strategy": {
                "position_size": 100,
                "order_action": "sell",
                "order_contracts": 1,
                "order_price": 51000,
                "order_id": "test_order_2",
                "market_position": "flat",
                "market_position_size": 0,
                "prev_market_position": "long",
                "prev_market_position_size": 1
            }
        }
    ]
    
    # Test each payload
    for i, payload in enumerate(test_cases, 1):
        try:
            response = requests.post(webhook_url, json=payload)
            logger.info(f"\nTest Case {i}:")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response: {response.text}")
            logger.info("-" * 50)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in Test Case {i}: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting webhook tests")
    test_webhook()
    logger.info("Completed webhook tests")
