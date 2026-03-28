from django.contrib import admin
from .models import Service, Stylist, Appointment, CustomerProfile, Gallery, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration_minutes', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']


@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'is_available']
    list_filter = ['is_available']
    filter_horizontal = ['services']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'service', 'stylist', 'appointment_date',
                    'appointment_time', 'status', 'payment_status']
    list_filter = ['status', 'payment_status', 'appointment_date']
    search_fields = ['customer__username', 'customer__first_name', 'customer__last_name']
    list_editable = ['status', 'payment_status']
    date_hierarchy = 'appointment_date'
    ordering = ['-appointment_date']


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']
    search_fields = ['user__username', 'phone']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'uploaded_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'is_featured', 'created_at']
    list_editable = ['is_featured']

admin.site.site_header = "Wasafi Beauty Salon  Admin"
admin.site.site_title = "Wasafi Admin"
admin.site.index_title = "Welcome to Wasafi Salon Management"
