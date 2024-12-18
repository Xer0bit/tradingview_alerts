import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import TradingViewAlert

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "alerts_group"

        # Join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_alert(self, alert_data):
        # Send alert to WebSocket client
        await self.send(text_data=json.dumps(alert_data))

    async def send_latest_alert(self):
        # Fetch the most recent alert from the database
        latest_alert = TradingViewAlert.objects.last()
        
        if latest_alert:
            data = {
                "symbol": latest_alert.symbol,
                "action": latest_alert.action,
                "message": latest_alert.message,
                "text_data": latest_alert.text_data,
                "received_at": latest_alert.received_at.isoformat()  # Ensure the datetime is serializable
            }
            # Send the data to the WebSocket
            await self.send(text_data=json.dumps({
                "status": "success",
                "latest_alert": data
            }))
        else:
            await self.send(text_data=json.dumps({
                "status": "error",
                "message": "No alert data available"
            }))
    
    # This function will be called to broadcast the latest alert every 1 second
    async def send_alert_periodically(self):
        while True:
            await self.send_latest_alert()
            await asyncio.sleep(1)  # Wait for 1 second before refreshing
