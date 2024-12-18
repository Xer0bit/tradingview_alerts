from django.db import models

class TradingViewAlert(models.Model):
    symbol = models.CharField(max_length=100, null=True, blank=True)
    action = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    text_data = models.TextField(null=True, blank=True)
    strategy = models.JSONField(default=dict, null=True, blank=True)  # Modified this line
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-received_at']
    
    def __str__(self):
        return f"Alert {self.id} - {self.received_at}"

class TradingAlert(models.Model):
    position_size = models.FloatField()
    order_action = models.CharField(max_length=10)
    order_contracts = models.FloatField()
    order_price = models.FloatField()
    order_id = models.CharField(max_length=100)
    market_position = models.CharField(max_length=10)
    market_position_size = models.FloatField()
    prev_market_position = models.CharField(max_length=10)
    prev_market_position_size = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
