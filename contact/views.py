from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import ContactMessage, ContactInfo, Newsletter
from .serializers import ContactMessageSerializer, ContactInfoSerializer, NewsletterSerializer
import threading
import requests


def send_email_async(subject, message, from_email, recipient_list):
    """Send email in a separate thread"""
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Email sending failed: {e}")


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save to database
        contact_message = serializer.save()
        
        # Send email asynchronously (non-blocking)
        subject = f"New Contact Message: {contact_message.subject}"
        message = f"""
New contact message received:

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone}
Subject: {contact_message.subject}

Message:
{contact_message.message}

Received at: {contact_message.created_at}
        """
        
        # Send email in background thread
        email_thread = threading.Thread(
            target=send_email_async,
            args=(subject, message, settings.EMAIL_HOST_USER, ['info@sundarmarbles.com'])
        )
        email_thread.daemon = True
        email_thread.start()
        
        # Return response immediately
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Your message has been sent successfully!', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ContactInfoView(generics.ListAPIView):
    queryset = ContactInfo.objects.filter(is_active=True)
    serializer_class = ContactInfoSerializer


class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newsletter = serializer.save()
        
        return Response(
            {'message': 'Successfully subscribed to newsletter!'},
            status=status.HTTP_201_CREATED
        )


@api_view(['POST'])
def send_to_whatsapp(request, message_id):
    """Send contact message to WhatsApp"""
    try:
        message = ContactMessage.objects.get(id=message_id)
        whatsapp_url = message.get_whatsapp_url()
        
        # Mark as sent to WhatsApp
        message.whatsapp_sent = True
        message.whatsapp_sent_at = timezone.now()
        message.save()
        
        return Response({
            'message': 'WhatsApp URL generated successfully',
            'whatsapp_url': whatsapp_url
        })
    except ContactMessage.DoesNotExist:
        return Response(
            {'error': 'Message not found'},
            status=status.HTTP_404_NOT_FOUND
        )
