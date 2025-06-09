from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myauth.models import UserProfile

class Command(BaseCommand):
    help = 'Creates user profiles for existing users'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            UserProfile.objects.get_or_create(user=user)
            self.stdout.write(f'Created profile for user {user.username}') 