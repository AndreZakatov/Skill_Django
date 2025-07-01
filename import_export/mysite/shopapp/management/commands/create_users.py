from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create users for fixtures'

    def handle(self, *args, **options):
        # Создаем пользователей с ID 1, 2, 3
        users_data = [
            {'id': 1, 'username': 'user1', 'email': 'user1@example.com'},
            {'id': 2, 'username': 'user2', 'email': 'user2@example.com'},
            {'id': 3, 'username': 'user3', 'email': 'user3@example.com'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                id=user_data['id'],
                defaults={
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'password': 'password123'  # Простой пароль для тестирования
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user {user.username} with ID {user.id}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {user.username} with ID {user.id} already exists')
                ) 