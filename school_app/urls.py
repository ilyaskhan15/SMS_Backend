from django.urls import path
from .views import Guardian

urlpatterns = [
    path('', Guardian)
]