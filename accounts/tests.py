from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_auto_creation(self):
        """Test that profile is auto-created when user signs up"""
        # Profile should be created automatically
        profile, created = Profile.objects.get_or_create(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.commute_radius_km, 10)  # default value
    
    def test_profile_str_representation(self):
        """Test profile string representation"""
        profile, created = Profile.objects.get_or_create(user=self.user)
        expected = f"{self.user.username}'s profile"
        self.assertEqual(str(profile), expected)

class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile, created = Profile.objects.get_or_create(user=self.user)
    
    def test_profile_detail_view(self):
        """Test profile detail view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testuser')  # Username is capitalized in template
    
    def test_profile_edit_view(self):
        """Test profile edit view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_profile_edit_save(self):
        """Test saving profile edits"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'headline': 'Test Headline',
            'skills': 'Python, Django, JavaScript',
            'education': 'Test University',
            'experience': 'Test Experience',
            'links': 'https://github.com/testuser',
            'is_public': True,
            'show_skills': True,
            'show_education': True,
            'show_experience': True,
            'show_links': True,
            'commute_radius_km': 25
        }
        response = self.client.post(reverse('accounts:profile_edit'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after save
        
        # Check that data was saved
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.headline, 'Test Headline')
        self.assertEqual(self.profile.skills, 'Python, Django, JavaScript')
        self.assertEqual(self.profile.commute_radius_km, 25)
    
    def test_public_profile_view(self):
        """Test public profile view respects privacy settings"""
        # Make profile public
        self.profile.is_public = True
        self.profile.show_skills = False  # Hide skills
        self.profile.save()
        
        response = self.client.get(reverse('accounts:public_profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Python, Django, JavaScript')  # Skills should be hidden
    
    def test_private_profile_access(self):
        """Test that private profiles are not accessible to others"""
        self.profile.is_public = False
        self.profile.save()
        
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Other user should not be able to access private profile
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('accounts:public_profile', args=['testuser']))
        self.assertEqual(response.status_code, 403)

class SignupTest(TestCase):
    def test_signup_creates_profile(self):
        """Test that signup automatically creates a profile"""
        client = Client()
        data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = client.post(reverse('accounts:signup'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after signup
        
        # Check that user and profile were created
        user = User.objects.get(username='newuser')
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)