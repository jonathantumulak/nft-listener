from django.db import models


class TransferEvent(models.Model):
    token_id = models.IntegerField(verbose_name="Token ID")
    from_address = models.CharField(verbose_name="From Address", max_length=42)
    to_address = models.CharField(verbose_name="To Address", max_length=42)
    tx_hash = models.CharField(verbose_name="Transaction Hash", max_length=66)
    block_number = models.PositiveBigIntegerField(verbose_name="Block Number")

    class Meta:
        app_label = "listener"
        verbose_name = "Transfer Event"
        verbose_name_plural = "Transfer Events"
