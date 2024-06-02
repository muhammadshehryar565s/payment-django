






from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.conf import settings

from django.http import JsonResponse

import stripe

from .models import Cardpayment
from .serializers import PaymentSerializer



stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(APIView):
    def post(self, request):
        try:
            token = request.data.get('token')
            if not token:
                return Response({'error': 'Missing token'}, status=400)

            amount = request.data.get('bill')  # Amount in cents
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Example charge',
                source=token,
            )
            return Response({'success': True})
        except stripe.error.CardError as e:
            return Response({'error': str(e)}, status=400)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=400)





@api_view(['POST'])
def payment_create(request):
    if request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return JsonResponse({'status': 'invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({'status': 'invalid signature'}, status=400)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            print('PaymentIntent was successful!')

        return JsonResponse({'status': 'success'}, status=200)