from rest_framework import serializers
from .models import ContactMessage, ContactInfo, Newsletter


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            'id', 'company_name', 'address', 'city', 'postal_code', 'country',
            'primary_phone', 'secondary_phone', 'whatsapp_number', 'email', 'website',
            'business_hours', 'facebook_url', 'instagram_url', 'youtube_url'
        ]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['id', 'email', 'name', 'subscribed_at']
        read_only_fields = ['id', 'subscribed_at']

    def create(self, validated_data):
        # Check if email already exists
        email = validated_data['email']
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults=validated_data
        )
        if not created and not newsletter.is_active:
            # Reactivate if previously unsubscribed
            newsletter.is_active = True
            newsletter.unsubscribed_at = None
            newsletter.save()
        return newsletter
