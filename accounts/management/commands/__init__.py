from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Add demo users with email addresses for testing'

    def handle(self, *args, **options):
        # Demo job seekers
        demo_users = [
            {
                'username': 'demo_seeker',
                'email': 'demo.seeker@example.com',
                'first_name': 'Demo',
                'last_name': 'Seeker',
                'user_type': 'job_seeker'
            },
            {
                'username': 'john_doe',
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'job_seeker'
            },
            {
                'username': 'jane_smith',
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'user_type': 'job_seeker'
            },
            {
                'username': 'mike_wilson',
                'email': 'mike.wilson@example.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'user_type': 'job_seeker'
            },
            {
                'username': 'sarah_jones',
                'email': 'sarah.jones@example.com',
                'first_name': 'Sarah',
                'last_name': 'Jones',
                'user_type': 'job_seeker'
            }
        ]

        for user_data in demo_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.username} ({user.email})')
                )
            else:
                # Update email if it's missing
                if not user.email:
                    user.email = user_data['email']
                    user.first_name = user_data['first_name']
                    user.last_name = user_data['last_name']
                    user.save()
                    self.stdout.write(
                        self.style.WARNING(f'Updated user: {user.username} ({user.email})')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'User already exists: {user.username}')
                    )

            # Create or update profile
            profile, profile_created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'user_type': user_data['user_type'],
                    'headline': f'{user_data["first_name"]} {user_data["last_name"]} - Software Developer',
                    'skills': 'Python, JavaScript, React, Django, SQL',
                    'education': 'Bachelor of Computer Science',
                    'experience': '2+ years of software development experience',
                    'is_public': True
                }
            )

            if profile_created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created profile for: {user.username}')
                )

        self.stdout.write(
            self.style.SUCCESS('Demo users with emails created successfully!')
        )
