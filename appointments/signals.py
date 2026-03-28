from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerProfile

@receiver(user_signed_up)
def populate_user_profile(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        data = sociallogin.account.extra_data

        # Get data from Google
        user.email = data.get('email', '')
        user.first_name = data.get('given_name', '')
        user.last_name = data.get('family_name', '')
        user.save()

        # Create profile if not exists
        CustomerProfile.objects.get_or_create(user=user)