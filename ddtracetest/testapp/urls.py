from django.urls import path
from .views import test_async_view

urlpatterns = [
    path('test-async/', test_async_view, name='test_async_view'),
]