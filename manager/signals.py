"""Signals to trigger on events"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from manager import models

UserModel = get_user_model()

# pylint: disable=unused-argument
@receiver(post_save, sender=UserModel)
def create_manager(sender, instance, created, **kwargs):
    """Create manager on the event a new user is created"""
    if not created:
        return
    models.Manager.objects.create(
        user=instance,
        first_name=instance.first_name,
        last_name=instance.last_name,
    )