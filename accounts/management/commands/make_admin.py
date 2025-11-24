from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Promote an existing user to admin (staff + superuser)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to promote to admin')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Success! {username} is now an admin!'))
            self.stdout.write(f'   - is_staff: {user.is_staff}')
            self.stdout.write(f'   - is_superuser: {user.is_superuser}')
            self.stdout.write(f'\nYou can now access the admin panel at /accounts/admin/')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Error: User "{username}" not found'))
            self.stdout.write('\nAvailable users:')
            for u in User.objects.all()[:10]:
                self.stdout.write(f'  - {u.username}')

