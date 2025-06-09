from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_avatar_directory_path(instance: "UserProfile", filename: str) -> str:
    return "users/user_{pk}/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename,
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_avatar_directory_path)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Profile for user {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)
