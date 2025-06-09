from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myauth.models import UserProfile

class Command(BaseCommand):
    help = 'Resets and recreates all user profiles'

    def handle(self, *args, **options):
        # Удаляем все существующие профили
        UserProfile.objects.all().delete()
        self.stdout.write('Deleted all existing profiles')

        # Создаем новые профили для всех пользователей
        users = User.objects.all()
        for user in users:
            UserProfile.objects.create(user=user)
            self.stdout.write(f'Created profile for user {user.username}') 