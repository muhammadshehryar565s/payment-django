# from app import views
# from django.urls import path
# from .views import PaymentView
# urlpatterns = [


#      path('payment/', views.payment_create, name='payment_create'),
#      path('payment/', PaymentView.as_view(), name='payment-view'),

    
    
#     # path('<slug:course_slug>/<slug:lesson_slug>/show_comment/', views.get_comments),
# ]



from django.urls import path
from .views import PaymentView, payment_create, StripeWebhookView

urlpatterns = [
    path('payment/', payment_create, name='payment_create'),
    path('payment/stripe/', PaymentView.as_view(), name='payment-view'),
    # path('api/payment/stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('payment/stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
