from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Job, JobApplication
from accounts.models import Profile

class JobModelTest(TestCase):
    def setUp(self):
        self.job = Job.objects.create(
            title='Test Developer',
            description='Test job description',
            location='Atlanta, GA',
            latitude=33.7490,
            longitude=-84.3880,
            salary_min=80000,
            salary_max=120000,
            is_remote=True,
            visa_sponsorship=True,
            company_name='Test Company'
        )
    
    def test_job_str_representation(self):
        """Test job string representation"""
        expected = "Test Developer at Test Company"
        self.assertEqual(str(self.job), expected)
    
    def test_job_ordering(self):
        """Test that jobs are ordered by created_at descending"""
        import time
        time.sleep(0.01)  # Small delay to ensure different timestamps
        job2 = Job.objects.create(
            title='Another Job',
            description='Another description',
            company_name='Another Company'
        )
        jobs = Job.objects.all()
        self.assertEqual(jobs[0], job2)  # Newer job first
        self.assertEqual(jobs[1], self.job)

class JobApplicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.job = Job.objects.create(
            title='Test Job',
            description='Test description',
            company_name='Test Company'
        )
    
    def test_application_str_representation(self):
        """Test application string representation"""
        application = JobApplication.objects.create(
            job=self.job,
            user=self.user,
            note='Test note'
        )
        expected = "testuser applied to Test Job"
        self.assertEqual(str(application), expected)
    
    def test_unique_together_constraint(self):
        """Test that users can't apply to the same job twice"""
        JobApplication.objects.create(job=self.job, user=self.user)
        
        # Try to create another application for the same job and user
        with self.assertRaises(Exception):  # Should raise IntegrityError
            JobApplication.objects.create(job=self.job, user=self.user)

class JobViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.profile.skills = 'Python, Django, JavaScript'
        self.profile.save()
        
        self.job = Job.objects.create(
            title='Python Developer',
            description='Looking for a Python developer with Django experience',
            location='Atlanta, GA',
            latitude=33.7490,
            longitude=-84.3880,
            salary_min=80000,
            salary_max=120000,
            is_remote=True,
            visa_sponsorship=True,
            company_name='TechCorp'
        )
    
    def test_job_list_view(self):
        """Test job list view with filters"""
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')
    
    def test_job_list_title_filter(self):
        """Test job list filtering by title"""
        response = self.client.get(reverse('jobs:list'), {'title': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')
        
        response = self.client.get(reverse('jobs:list'), {'title': 'Java'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Python Developer')
    
    def test_job_application_view(self):
        """Test job application functionality"""
        self.client.login(username='testuser', password='testpass123')
        
        # Apply to job
        response = self.client.post(reverse('jobs:apply', args=[self.job.pk]), {
            'note': 'I am very interested in this position!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after apply
        
        # Check that application was created
        application = JobApplication.objects.get(job=self.job, user=self.user)
        self.assertEqual(application.note, 'I am very interested in this position!')
        self.assertEqual(application.status, 'applied')
    
    def test_duplicate_application_prevention(self):
        """Test that users can't apply to the same job twice"""
        self.client.login(username='testuser', password='testpass123')
        
        # First application
        self.client.post(reverse('jobs:apply', args=[self.job.pk]))
        
        # Second application should show warning
        response = self.client.post(reverse('jobs:apply', args=[self.job.pk]))
        self.assertEqual(response.status_code, 302)
        
        # Should only have one application
        applications = JobApplication.objects.filter(job=self.job, user=self.user)
        self.assertEqual(applications.count(), 1)
    
    def test_recommended_jobs_view(self):
        """Test recommended jobs based on skills"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('jobs:recommended'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')
    
    def test_job_map_view(self):
        """Test job map view"""
        response = self.client.get(reverse('jobs:map'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Job Map')
        self.assertContains(response, 'const jobs =')  # Should contain job data as JSON
