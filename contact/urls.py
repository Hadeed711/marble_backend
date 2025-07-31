from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('message/', views.ContactMessageCreateView.as_view(), name='message-create'),
    path('info/', views.ContactInfoView.as_view(), name='contact-info'),
    path('newsletter/', views.NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('whatsapp/<int:message_id>/', views.send_to_whatsapp, name='send-to-whatsapp'),
]
