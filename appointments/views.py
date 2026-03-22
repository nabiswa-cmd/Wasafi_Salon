from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Service, Appointment, Stylist, Gallery, Testimonial, CustomerProfile
from .forms import CustomerRegistrationForm, LoginForm, AppointmentBookingForm, ProfileUpdateForm
import datetime
from .mpesa import stk_push


def home(request):
    services = Service.objects.filter(is_active=True)[:6]
    testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    stylists = Stylist.objects.filter(is_available=True)[:3]
    gallery = Gallery.objects.all()[:8]
    context = {
        'services': services,
        'testimonials': testimonials,
        'stylists': stylists,
        'gallery': gallery,
    }
    return render(request, 'appointments/home.html', context)


def services_list(request):
    category = request.GET.get('category', '')
    services = Service.objects.filter(is_active=True)
    if category:
        services = services.filter(category=category)
    categories = Service.CATEGORY_CHOICES
    context = {'services': services, 'categories': categories, 'active_category': category}
    return render(request, 'appointments/services.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, 'appointments/service_detail.html', {'service': service})



def about(request):
    stylists = Stylist.objects.filter(is_available=True)
    
    values = [
        {"icon": "bi-award", "title": "Quality First", "desc": "We use only premium products."},
        {"icon": "bi-heart", "title": "Customer Care", "desc": "We value every client."},
        {"icon": "bi-star", "title": "Excellence", "desc": "We deliver top services."},
    ]

    return render(request, 'appointments/about.html', {
        'stylists': stylists,
        'values': values
    })

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you! Your message has been received. We will contact you soon.')
        return redirect('contact')
    return render(request, 'appointments/contact.html')


def gallery_view(request):
    images = Gallery.objects.all()
    return render(request, 'appointments/gallery.html', {'images': images})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Wasafi Beauty Salon, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'appointments/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'appointments/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(customer=request.user).order_by('-appointment_date')
    upcoming = appointments.filter(
        appointment_date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    )
    past = appointments.filter(appointment_date__lt=timezone.now().date())
    context = {
        'appointments': appointments,
        'upcoming': upcoming,
        'past': past,
        'total_appointments': appointments.count(),
        'completed_appointments': appointments.filter(status='completed').count(),
    }
    return render(request, 'appointments/dashboard.html', context)



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def book_appointment(request):
    service_id = request.GET.get('service')
    initial = {}

    if service_id:
        try:
            initial['service'] = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            pass

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = request.user
            appointment.status = 'pending'
            appointment.payment_status = 'unpaid'
            appointment.save()

            # ✅ GET PHONE
            try:
                phone = request.user.profile.phone
            except:
                return JsonResponse({
                    "status": "error",
                    "message": "Please update your profile with phone number"
                })

            # ✅ FORMAT PHONE
            if phone.startswith("0"):
                phone = "254" + phone[1:]

            # ✅ M-PESA
            if appointment.payment_method == "M-Pesa":
                stk_push(phone, appointment.total_price, appointment.id)

                return JsonResponse({
                    "status": "waiting",
                    "appointment_id": appointment.id
                })

            # ✅ NON MPESA
            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "error", "message": "Invalid form"})

    else:
        form = AppointmentBookingForm(initial=initial)

    return render(request, 'appointments/book_appointment.html', {'form': form})
def check_payment(request, id):
    appointment = Appointment.objects.get(id=id)

    if appointment.payment_status == "paid":
        return JsonResponse({"status": "paid"})
    elif appointment.status == "cancelled":
        return JsonResponse({"status": "failed"})
    else:
        return JsonResponse({"status": "pending"})
    
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)

    try:
        result = data['Body']['stkCallback']

        if result['ResultCode'] == 0:
            metadata = result['CallbackMetadata']['Item']

            appointment_id = None

            for item in metadata:
                if item['Name'] == "AccountReference":
                    appointment_id = item['Value']

            if appointment_id:
                appointment = Appointment.objects.get(id=appointment_id)

                appointment.payment_status = "paid"
                appointment.status = "confirmed"
                appointment.save()

                print(" PAYMENT SUCCESS")

        else:
            print("SORRY!! PAYMENT FAILED")

    except Exception as e:
        print("ERROR:", e)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, customer=request.user)
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.warning(request, 'Your appointment has been cancelled.')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')
    return redirect('dashboard')


@login_required
def profile(request):
    profile_obj, created = CustomerProfile.objects.get_or_create(
        user=request.user, defaults={'phone': ''}
    )
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile_obj)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(
            instance=profile_obj,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )
    return render(request, 'appointments/profile.html', {'form': form, 'profile': profile_obj})


def get_available_slots(request):
    """AJAX endpoint to get available time slots for a date/stylist combo."""
    date_str = request.GET.get('date')
    stylist_id = request.GET.get('stylist')
    if not date_str:
        return JsonResponse({'slots': []})
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'slots': []})

    booked_times = Appointment.objects.filter(
        appointment_date=date,
        stylist_id=stylist_id if stylist_id else None,
        status__in=['pending', 'confirmed']
    ).values_list('appointment_time', flat=True)

    all_slots = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
        '12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
        '15:00', '15:30', '16:00', '16:30', '17:00'
    ]
    booked_strs = [t.strftime('%H:%M') for t in booked_times]
    available = [s for s in all_slots if s not in booked_strs]
    return JsonResponse({'available_slots': available, 'booked_slots': booked_strs})
