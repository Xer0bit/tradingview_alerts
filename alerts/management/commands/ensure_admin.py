from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates or updates the admin user'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'tradingview123'
        email = 'admin@example.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Admin user "{username}" already exists')
            admin_user = User.objects.get(username=username)
            admin_user.set_password(password)
            admin_user.save()
            self.stdout.write(f'Updated password for "{username}"')
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f'Created admin user "{username}"')
