from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser  # Use CustomUser instead of User if you're using a custom user model

@receiver(post_save, sender=CustomUser)  # Replace User with CustomUser
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)  # Replace User with CustomUser
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
