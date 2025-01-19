# payments/urls.py
from django.urls import path
from .views import CreateCheckoutSession, PaymentSuccess, PaymentFailed

urlpatterns = [
    path("create-checkout-session/", CreateCheckoutSession.as_view(),
         name="create_checkout_session"),
    path("success/", PaymentSuccess.as_view(), name="payment_success"),
    path("failed/", PaymentFailed.as_view(), name="payment_failed"),
]
