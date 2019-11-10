from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from random_username.generate import generate_username


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_handle = models.CharField(max_length=50, unique=True)
    # profile_picture = models.ImageField(default='/static/user.png')
    # background_picture = models.ImageField(default='/static/user.png')

    def __str__(self):
        return self.user_handle

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, user_handle=generate_username(1)[0])

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

