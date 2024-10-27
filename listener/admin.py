from django.contrib import admin
from listener.models import TransferEvent


class TransferEventAdmin(admin.ModelAdmin):
    list_display = (
        "token_id",
        "from_address",
        "to_address",
        "tx_hash",
        "block_number",
    )


admin.site.register(TransferEvent, TransferEventAdmin)
