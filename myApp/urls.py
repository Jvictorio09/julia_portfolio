from . import views
from django.urls import path
from django.http import HttpResponse

urlpatterns = [
    path('', views.home, name='home'),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("assistant/chat/", views.ai_chat, name="ai_chat"),
]