from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Existing pages
    path("", views.home, name="home"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("assistant/chat/", views.ai_chat, name="ai_chat"),

    # Donation widget + Stripe
    path("donate/widget/", views.widget, name="donation_widget"),
    path("donate/create-checkout-session/", views.CreateCheckoutSessionView.as_view(), name="create_checkout_session"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("donate/success/", TemplateView.as_view(template_name="donate_success.html"), name="donate_success"),
    path("donate/cancel/", TemplateView.as_view(template_name="donate_cancel.html"), name="donate_cancel"),
]
