from django.urls import path

from .views import PayView, PayCallbackView

app_name = 'payment'

urlpatterns = [
    path('pay/', PayView.as_view(), name='pay_view'),
    path('pay-callback/', PayCallbackView.as_view(), name='pay_callback'),
]