from django.urls import path
from django.contrib.auth.decorators import login_required
from . views import ClientsRR

urlpatterns = [
    path('', login_required(ClientsRR.as_view()), name="clients"),
]
