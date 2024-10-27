from django.urls import path
from listener import views


urlpatterns = [
    path(
        "filter-transfer-events/<int:token_id>",
        views.TransferEventView.as_view(),
        name="listener.TransferEventView",
    ),
]
