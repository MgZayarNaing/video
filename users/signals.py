from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now

@receiver(user_logged_out)
def update_last_logout(sender, request, user, **kwargs):
    user.last_logout = now()
    user.save()
