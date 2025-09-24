from django.core.management.base import BaseCommand
from jobs.models import Job

class Command(BaseCommand):
    help = 'Populate database with sample job data'

    def handle(self, *args, **options):
        # Sample jobs with Atlanta area coordinates
        sample_jobs = [
            {
                'title': 'Software Engineer',
                'description': 'We are looking for a talented Software Engineer to join our team. You will work on cutting-edge web applications using Python, Django, and React. Experience with cloud platforms and DevOps practices is a plus.',
                'location': 'Atlanta, GA',
                'latitude': 33.7490,
                'longitude': -84.3880,
                'salary_min': 80000,
                'salary_max': 120000,
                'company_name': 'TechCorp',
                'company_logo': 'https://via.placeholder.com/100x50/007bff/ffffff?text=TechCorp',
                'is_remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'Data Scientist',
                'description': 'Join our data science team to build machine learning models and analyze large datasets. You will work with Python, TensorFlow, and cloud computing platforms. PhD in a quantitative field preferred.',
                'location': 'Atlanta, GA',
                'latitude': 33.7600,
                'longitude': -84.3800,
                'salary_min': 90000,
                'salary_max': 140000,
                'company_name': 'DataFlow Inc',
                'company_logo': 'https://via.placeholder.com/100x50/28a745/ffffff?text=DataFlow',
                'is_remote': True,
                'visa_sponsorship': True
            },
            {
                'title': 'Frontend Developer',
                'description': 'Create beautiful and responsive user interfaces using React, TypeScript, and modern CSS. You will collaborate with designers and backend developers to deliver exceptional user experiences.',
                'location': 'Atlanta, GA',
                'latitude': 33.7400,
                'longitude': -84.3900,
                'salary_min': 70000,
                'salary_max': 100000,
                'company_name': 'WebCraft',
                'company_logo': 'https://via.placeholder.com/100x50/ffc107/000000?text=WebCraft',
                'is_remote': False,
                'visa_sponsorship': False
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Manage our cloud infrastructure and deployment pipelines. Experience with AWS, Docker, Kubernetes, and CI/CD required. You will ensure our systems are scalable, secure, and reliable.',
                'location': 'Atlanta, GA',
                'latitude': 33.7500,
                'longitude': -84.3850,
                'salary_min': 85000,
                'salary_max': 130000,
                'company_name': 'CloudScale',
                'company_logo': 'https://via.placeholder.com/100x50/17a2b8/ffffff?text=CloudScale',
                'is_remote': True,
                'visa_sponsorship': True
            },
            {
                'title': 'Product Manager',
                'description': 'Lead product development from conception to launch. Work with engineering, design, and business teams to define product requirements and roadmap. MBA or technical background preferred.',
                'location': 'Atlanta, GA',
                'latitude': 33.7550,
                'longitude': -84.3950,
                'salary_min': 100000,
                'salary_max': 150000,
                'company_name': 'InnovateTech',
                'company_logo': 'https://via.placeholder.com/100x50/dc3545/ffffff?text=InnovateTech',
                'is_remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'UX Designer',
                'description': 'Design intuitive and engaging user experiences for our mobile and web applications. You will conduct user research, create wireframes and prototypes, and collaborate with development teams.',
                'location': 'Atlanta, GA',
                'latitude': 33.7450,
                'longitude': -84.3750,
                'salary_min': 65000,
                'salary_max': 95000,
                'company_name': 'DesignStudio',
                'company_logo': 'https://via.placeholder.com/100x50/6f42c1/ffffff?text=DesignStudio',
                'is_remote': True,
                'visa_sponsorship': False
            },
            {
                'title': 'Backend Developer',
                'description': 'Build robust and scalable backend services using Python, Django, and PostgreSQL. You will design APIs, optimize database queries, and implement security best practices.',
                'location': 'Atlanta, GA',
                'latitude': 33.7650,
                'longitude': -84.4000,
                'salary_min': 75000,
                'salary_max': 110000,
                'company_name': 'BackendPro',
                'company_logo': 'https://via.placeholder.com/100x50/20c997/ffffff?text=BackendPro',
                'is_remote': False,
                'visa_sponsorship': True
            },
            {
                'title': 'Full Stack Developer',
                'description': 'Work on both frontend and backend development using modern technologies. You will build complete web applications from database design to user interface implementation.',
                'location': 'Atlanta, GA',
                'latitude': 33.7350,
                'longitude': -84.3700,
                'salary_min': 80000,
                'salary_max': 120000,
                'company_name': 'FullStack Solutions',
                'company_logo': 'https://via.placeholder.com/100x50/fd7e14/ffffff?text=FullStack',
                'is_remote': True,
                'visa_sponsorship': True
            }
        ]

        # Clear existing jobs
        Job.objects.all().delete()
        self.stdout.write('Cleared existing jobs...')

        # Create sample jobs
        for job_data in sample_jobs:
            Job.objects.create(**job_data)
            self.stdout.write(f'Created job: {job_data["title"]} at {job_data["company_name"]}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(sample_jobs)} sample jobs!')
        )
