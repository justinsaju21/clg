
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser non-interactively if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING('Superuser details not found in env vars. Skipping.'))
            return

        if not User.objects.filter(username=username).exists():
            self.stdout.write(f'Creating superuser {username}...')
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created!'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists.'))
