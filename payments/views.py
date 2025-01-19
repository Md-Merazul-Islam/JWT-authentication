from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import stripe
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        amount = int(data.get("amount", 0)) * 100  # Convert to cents
        currency = data.get("currency", "usd")
        user = request.user if request.user.is_authenticated else None

        try:
            # Create Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": currency,
                            "product_data": {"name": "Product Purchase"},
                            "unit_amount": amount,
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=f"{settings.DOMAIN}/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.DOMAIN}/payments/failed",
            )

            # Create Payment record
            payment = Payment.objects.create(
                user=user,
                amount=amount / 100,
                payment_intent_id=session["id"],
                currency=currency,
            )

            return Response({"checkout_url": session["url"]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentSuccess(APIView):
    def get(self, request):
        session_id = request.GET.get("session_id")
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent = session.get("id")
            payment = Payment.objects.get(payment_intent_id=payment_intent)
            payment.is_paid = True
            payment.save()

            return Response({"message": "Payment successful!"}, status=status.HTTP_200_OK)
        except stripe.error.InvalidRequestError:
            return Response({"error": "Invalid session ID."}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)


class PaymentFailed(APIView):
    def get(self, request):
        return Response({"message": "Payment failed!"}, status=status.HTTP_200_OK)
