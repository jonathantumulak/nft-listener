from django.db.models import QuerySet
from django.http import JsonResponse
from django.views.generic.base import View
from listener.models import TransferEvent


class TransferEventView(View):
    """Basic view to list TransferEvents filtered by `token_id` and return
    as json
    """

    model = TransferEvent

    @property
    def queryset(self) -> QuerySet:
        return self.model.objects.all()

    def get_queryset(self, **kwargs) -> QuerySet:
        return self.queryset.filter(token_id=kwargs["token_id"])

    def get(self, *args, **kwargs) -> JsonResponse:
        """Get values queryset and return JsonResponse"""
        queryset = self.get_queryset(**kwargs)

        return JsonResponse(list(queryset.values()), safe=False)
