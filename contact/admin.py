from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ContactMessage, ContactInfo, Newsletter


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'priority', 'whatsapp_status', 'created_at']
    list_filter = ['status', 'priority', 'whatsapp_sent', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'whatsapp_sent_at', 'whatsapp_link']
    ordering = ['-created_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Management', {
            'fields': ('status', 'priority', 'admin_notes')
        }),
        ('WhatsApp Integration', {
            'fields': ('whatsapp_sent', 'whatsapp_sent_at', 'whatsapp_link'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'read_at'),
            'classes': ('collapse',)
        }),
    )

    def whatsapp_status(self, obj):
        if obj.whatsapp_sent:
            return format_html('<span style="color: green;">✓ Sent</span>')
        return format_html('<span style="color: orange;">⏳ Pending</span>')
    whatsapp_status.short_description = "WhatsApp"

    def whatsapp_link(self, obj):
        url = obj.get_whatsapp_url()
        return format_html('<a href="{}" target="_blank" class="button">Send to WhatsApp</a>', url)
    whatsapp_link.short_description = "WhatsApp Link"

    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_closed']

    def mark_as_read(self, request, queryset):
        for message in queryset:
            message.mark_as_read()
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')
        self.message_user(request, f"{queryset.count()} messages marked as replied.")
    mark_as_replied.short_description = "Mark selected messages as replied"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, f"{queryset.count()} messages marked as closed.")
    mark_as_closed.short_description = "Mark selected messages as closed"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email', 'primary_phone', 'city', 'is_active', 'updated_at']
    list_filter = ['is_active', 'country', 'city']
    search_fields = ['company_name', 'email', 'address']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'address', 'city', 'postal_code', 'country')
        }),
        ('Contact Details', {
            'fields': ('primary_phone', 'secondary_phone', 'whatsapp_number', 'email', 'website')
        }),
        ('Business Information', {
            'fields': ('business_hours',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    ordering = ['-subscribed_at']

    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f"{queryset.count()} subscriptions activated.")
    mark_as_active.short_description = "Activate selected subscriptions"

    def mark_as_inactive(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f"{queryset.count()} subscriptions deactivated.")
    mark_as_inactive.short_description = "Deactivate selected subscriptions"
