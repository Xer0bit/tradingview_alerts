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
