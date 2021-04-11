from django.db import models


class Coin(models.Model):
    timestamp = models.IntegerField()
    pair = models.CharField(max_length=10)
    mms_20 = models.FloatField()
    mms_50 = models.FloatField()
    mms_200 = models.FloatField()

    def __str__(self):
        return f"Timestamp {self.timestamp} - Crypto: {self.pair}"

    class Meta:
        verbose_name_plural = "coins"
        # Ensures the unique entry for that pair on that day
        constraints = [
            models.UniqueConstraint(fields=['timestamp', 'pair'], name='unique_entry')
        ]
