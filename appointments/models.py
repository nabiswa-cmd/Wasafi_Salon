from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('hair', 'Hair Services'),
        ('nails', 'Nail Services'),
        ('skin', 'Skin & Beauty'),
        ('massage', 'Massage & Spa'),
        ('makeup', 'Makeup'),
    ]
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='hair')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Duration in minutes")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - KSh {self.price}"


class Stylist(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='stylists/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    services = models.ManyToManyField(Service, related_name='stylists')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments')
    stylist = models.ForeignKey(Stylist, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=50, blank=True, default='M-Pesa')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        unique_together = ['stylist', 'appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.customer.get_full_name()} - {self.service.name} on {self.appointment_date}"

    @property
    def total_price(self):
        return self.service.price


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


class Gallery(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gallery/')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"

from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        import appointments.signals