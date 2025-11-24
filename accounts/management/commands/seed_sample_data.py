"""
Management command to seed comprehensive sample data for testing all user stories
Usage: python manage.py seed_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile, RecruiterProfile, Message, Education, WorkExperience
from jobs.models import Job, JobApplication
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Seeds database with comprehensive sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))

        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Cleaning existing sample data...')
        User.objects.filter(username__startswith='demo_').delete()

        # Create sample data
        self.create_job_seekers()
        self.create_recruiters()
        self.create_jobs()
        self.create_applications()
        self.create_messages()

        self.stdout.write(self.style.SUCCESS('[SUCCESS] Sample data seeding completed!'))
        self.print_summary()

    def create_job_seekers(self):
        """Create sample job seeker accounts with profiles"""
        self.stdout.write('Creating job seekers...')

        job_seekers_data = [
            {
                'username': 'demo_alice',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'password': 'password123',
                'profile': {
                    'headline': 'Full Stack Developer | React & Python Expert',
                    'skills': 'Python, Django, React, JavaScript, PostgreSQL, Docker, AWS, Git, REST APIs, CI/CD',
                    'location': 'Atlanta, GA',
                    'latitude': 33.7490,
                    'longitude': -84.3880,
                },
                'education': [
                    {
                        'school_name': 'Georgia Institute of Technology',
                        'degree': 'Bachelor of Science',
                        'field_of_study': 'Computer Science',
                        'gpa': 3.85,
                        'start_date': '2018-08-15',
                        'end_date': '2022-05-10',
                        'description': 'Concentration in Machine Learning. Dean\'s List all semesters. President of Women in Computing.',
                    },
                    {
                        'school_name': 'Georgia Institute of Technology',
                        'degree': 'Master of Science',
                        'field_of_study': 'Computer Science',
                        'gpa': 3.92,
                        'start_date': '2022-08-20',
                        'end_date': '2024-05-15',
                        'description': 'Specialization in Software Engineering. TA for Web Development course.',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'Software Engineering Intern',
                        'company_name': 'Google',
                        'location': 'Mountain View, CA',
                        'start_date': '2021-06-01',
                        'end_date': '2021-08-31',
                        'description': 'Developed features for Google Search using Python and C++. Improved search result ranking algorithm by 15%.',
                    },
                    {
                        'job_title': 'Full Stack Developer',
                        'company_name': 'Tech Startup Inc',
                        'location': 'Atlanta, GA',
                        'start_date': '2024-06-01',
                        'is_current': True,
                        'description': 'Building scalable web applications using React and Django. Led migration to microservices architecture.',
                    }
                ]
            },
            {
                'username': 'demo_bob',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'password': 'password123',
                'profile': {
                    'headline': 'Data Scientist | ML & AI Enthusiast',
                    'skills': 'Python, Machine Learning, TensorFlow, PyTorch, SQL, Pandas, NumPy, Scikit-learn, Data Visualization, Statistics',
                    'location': 'San Francisco, CA',
                    'latitude': 37.7749,
                    'longitude': -122.4194,
                },
                'education': [
                    {
                        'school_name': 'Stanford University',
                        'degree': 'Master of Science',
                        'field_of_study': 'Data Science',
                        'gpa': 3.78,
                        'start_date': '2020-09-01',
                        'end_date': '2022-06-15',
                        'description': 'Thesis on deep learning for natural language processing. Published 2 conference papers.',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'Data Scientist',
                        'company_name': 'Meta',
                        'location': 'Menlo Park, CA',
                        'start_date': '2022-07-01',
                        'is_current': True,
                        'description': 'Building recommendation systems for Facebook using deep learning. Improved user engagement by 20%.',
                    }
                ]
            },
            {
                'username': 'demo_carol',
                'email': 'carol@example.com',
                'first_name': 'Carol',
                'last_name': 'Williams',
                'password': 'password123',
                'profile': {
                    'headline': 'Frontend Developer | UI/UX Specialist',
                    'skills': 'JavaScript, React, Vue.js, HTML, CSS, TypeScript, Figma, Responsive Design, Accessibility, Performance Optimization',
                    'location': 'New York, NY',
                    'latitude': 40.7128,
                    'longitude': -74.0060,
                },
                'education': [
                    {
                        'school_name': 'New York University',
                        'degree': 'Bachelor of Arts',
                        'field_of_study': 'Digital Media Design',
                        'gpa': 3.65,
                        'start_date': '2017-09-01',
                        'end_date': '2021-05-20',
                        'description': 'Focus on interactive design and user experience.',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'Frontend Developer',
                        'company_name': 'Adobe',
                        'location': 'New York, NY',
                        'start_date': '2021-06-01',
                        'end_date': '2023-12-31',
                        'description': 'Developed responsive web interfaces for Creative Cloud applications.',
                    },
                    {
                        'job_title': 'Senior UI Developer',
                        'company_name': 'Spotify',
                        'location': 'New York, NY',
                        'start_date': '2024-01-15',
                        'is_current': True,
                        'description': 'Leading frontend development for music discovery features. Mentoring junior developers.',
                    }
                ]
            },
            {
                'username': 'demo_david',
                'email': 'david@example.com',
                'first_name': 'David',
                'last_name': 'Martinez',
                'password': 'password123',
                'profile': {
                    'headline': 'DevOps Engineer | Cloud & Infrastructure Expert',
                    'skills': 'AWS, Docker, Kubernetes, Terraform, Jenkins, CI/CD, Linux, Bash, Monitoring, Networking',
                    'location': 'Austin, TX',
                    'latitude': 30.2672,
                    'longitude': -97.7431,
                },
                'education': [
                    {
                        'school_name': 'University of Texas at Austin',
                        'degree': 'Bachelor of Science',
                        'field_of_study': 'Computer Engineering',
                        'gpa': 3.55,
                        'start_date': '2016-08-25',
                        'end_date': '2020-05-15',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'DevOps Engineer',
                        'company_name': 'Amazon Web Services',
                        'location': 'Austin, TX',
                        'start_date': '2020-06-01',
                        'is_current': True,
                        'description': 'Managing cloud infrastructure and deployment pipelines. Reduced deployment time by 40%.',
                    }
                ]
            },
            {
                'username': 'demo_emma',
                'email': 'emma@example.com',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'password': 'password123',
                'profile': {
                    'headline': 'Product Manager | SaaS & Mobile Apps',
                    'skills': 'Product Management, Agile, Scrum, User Research, Analytics, Roadmapping, Jira, SQL, A/B Testing',
                    'location': 'Seattle, WA',
                    'latitude': 47.6062,
                    'longitude': -122.3321,
                },
                'education': [
                    {
                        'school_name': 'University of Washington',
                        'degree': 'MBA',
                        'field_of_study': 'Business Administration',
                        'gpa': 3.88,
                        'start_date': '2019-09-01',
                        'end_date': '2021-06-10',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'Product Manager',
                        'company_name': 'Microsoft',
                        'location': 'Seattle, WA',
                        'start_date': '2021-07-01',
                        'is_current': True,
                        'description': 'Leading product development for Teams collaboration features. Launched 3 major features.',
                    }
                ]
            },
            {
                'username': 'demo_frank',
                'email': 'frank@example.com',
                'first_name': 'Frank',
                'last_name': 'Garcia',
                'password': 'password123',
                'profile': {
                    'headline': 'Backend Engineer | Microservices & APIs',
                    'skills': 'Java, Spring Boot, Microservices, REST APIs, GraphQL, MongoDB, Redis, Kafka, RabbitMQ',
                    'location': 'Boston, MA',
                    'latitude': 42.3601,
                    'longitude': -71.0589,
                },
                'education': [
                    {
                        'school_name': 'MIT',
                        'degree': 'Bachelor of Science',
                        'field_of_study': 'Software Engineering',
                        'gpa': 3.92,
                        'start_date': '2018-09-01',
                        'end_date': '2022-05-30',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'Backend Engineer',
                        'company_name': 'Stripe',
                        'location': 'Boston, MA',
                        'start_date': '2022-06-15',
                        'is_current': True,
                        'description': 'Building payment processing APIs. Handling 1M+ transactions per day.',
                    }
                ]
            },
            {
                'username': 'demo_grace',
                'email': 'grace@example.com',
                'first_name': 'Grace',
                'last_name': 'Lee',
                'password': 'password123',
                'profile': {
                    'headline': 'Mobile Developer | iOS & Android',
                    'skills': 'Swift, Kotlin, React Native, iOS Development, Android Development, Mobile UI/UX, Core Data, Firebase',
                    'location': 'Los Angeles, CA',
                    'latitude': 34.0522,
                    'longitude': -118.2437,
                },
                'education': [
                    {
                        'school_name': 'UCLA',
                        'degree': 'Bachelor of Science',
                        'field_of_study': 'Computer Science',
                        'gpa': 3.70,
                        'start_date': '2017-09-20',
                        'end_date': '2021-06-15',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'iOS Developer',
                        'company_name': 'Snap Inc',
                        'location': 'Los Angeles, CA',
                        'start_date': '2021-07-01',
                        'is_current': True,
                        'description': 'Developing features for Snapchat iOS app. Optimized app performance by 30%.',
                    }
                ]
            },
            {
                'username': 'demo_henry',
                'email': 'henry@example.com',
                'first_name': 'Henry',
                'last_name': 'Chen',
                'password': 'password123',
                'profile': {
                    'headline': 'Security Engineer | Cybersecurity Specialist',
                    'skills': 'Cybersecurity, Penetration Testing, Network Security, SIEM, Firewall, Cryptography, Python, Security Audits',
                    'location': 'Washington, DC',
                    'latitude': 38.9072,
                    'longitude': -77.0369,
                },
                'education': [
                    {
                        'school_name': 'Carnegie Mellon University',
                        'degree': 'Master of Science',
                        'field_of_study': 'Information Security',
                        'gpa': 3.95,
                        'start_date': '2020-08-25',
                        'end_date': '2022-05-20',
                    }
                ],
                'experience': [
                    {
                        'job_title': 'Security Engineer',
                        'company_name': 'Cloudflare',
                        'location': 'Washington, DC',
                        'start_date': '2022-06-01',
                        'is_current': True,
                        'description': 'Protecting infrastructure from cyber attacks. Implemented security policies reducing vulnerabilities by 60%.',
                    }
                ]
            },
        ]

        for data in job_seekers_data:
            # Create user
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )

            # Create profile
            profile = Profile.objects.create(
                user=user,
                user_type='job_seeker',
                **data['profile']
            )

            # Create education entries
            for idx, edu in enumerate(data.get('education', [])):
                Education.objects.create(
                    profile=profile,
                    order=idx,
                    start_date=datetime.strptime(edu['start_date'], '%Y-%m-%d').date() if 'start_date' in edu else None,
                    end_date=datetime.strptime(edu['end_date'], '%Y-%m-%d').date() if 'end_date' in edu else None,
                    school_name=edu['school_name'],
                    degree=edu['degree'],
                    field_of_study=edu.get('field_of_study', ''),
                    gpa=edu.get('gpa'),
                    description=edu.get('description', ''),
                )

            # Create work experience entries
            for idx, exp in enumerate(data.get('experience', [])):
                WorkExperience.objects.create(
                    profile=profile,
                    order=idx,
                    job_title=exp['job_title'],
                    company_name=exp['company_name'],
                    location=exp.get('location', ''),
                    start_date=datetime.strptime(exp['start_date'], '%Y-%m-%d').date(),
                    end_date=datetime.strptime(exp['end_date'], '%Y-%m-%d').date() if 'end_date' in exp else None,
                    is_current=exp.get('is_current', False),
                    description=exp.get('description', ''),
                )

            self.stdout.write(f'  [OK] Created job seeker: {user.username}')

    def create_recruiters(self):
        """Create sample recruiter accounts"""
        self.stdout.write('Creating recruiters...')

        recruiters_data = [
            {
                'username': 'demo_recruiter_google',
                'email': 'recruiter@google.com',
                'first_name': 'Sarah',
                'last_name': 'Thompson',
                'password': 'password123',
                'company': {
                    'company_name': 'Google',
                    'company_description': 'Leading technology company focused on search, advertising, and cloud computing.',
                    'company_website': 'https://careers.google.com',
                    'company_logo': 'https://logo.clearbit.com/google.com',
                    'phone': '(650) 253-0000',
                    'address': '1600 Amphitheatre Parkway, Mountain View, CA 94043',
                    'industry': 'Technology',
                    'company_size': '100000+',
                    'is_verified': True,
                }
            },
            {
                'username': 'demo_recruiter_amazon',
                'email': 'recruiter@amazon.com',
                'first_name': 'Michael',
                'last_name': 'Anderson',
                'password': 'password123',
                'company': {
                    'company_name': 'Amazon',
                    'company_description': 'E-commerce and cloud computing leader. We are Earth\'s most customer-centric company.',
                    'company_website': 'https://www.amazon.jobs',
                    'company_logo': 'https://logo.clearbit.com/amazon.com',
                    'phone': '(206) 266-1000',
                    'address': '410 Terry Avenue North, Seattle, WA 98109',
                    'industry': 'Technology / E-commerce',
                    'company_size': '100000+',
                    'is_verified': True,
                }
            },
            {
                'username': 'demo_recruiter_startup',
                'email': 'recruiter@techstartup.com',
                'first_name': 'Jessica',
                'last_name': 'Park',
                'password': 'password123',
                'company': {
                    'company_name': 'TechFlow Solutions',
                    'company_description': 'Fast-growing fintech startup revolutionizing payment processing for small businesses.',
                    'company_website': 'https://techflow.example.com',
                    'phone': '(404) 555-0123',
                    'address': '123 Peachtree St, Atlanta, GA 30303',
                    'industry': 'Fintech',
                    'company_size': '50-200',
                    'is_verified': False,
                }
            },
        ]

        for data in recruiters_data:
            # Create user
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )

            # Create profile
            Profile.objects.create(
                user=user,
                user_type='recruiter',
                location='N/A - Recruiter',
            )

            # Create recruiter profile
            RecruiterProfile.objects.create(
                user=user,
                **data['company']
            )

            self.stdout.write(f'  [OK] Created recruiter: {user.username} ({data["company"]["company_name"]})')

    def create_jobs(self):
        """Create sample job postings"""
        self.stdout.write('Creating job postings...')

        # Get recruiters
        google_recruiter = User.objects.get(username='demo_recruiter_google')
        amazon_recruiter = User.objects.get(username='demo_recruiter_amazon')
        startup_recruiter = User.objects.get(username='demo_recruiter_startup')

        jobs_data = [
            {
                'title': 'Senior Full Stack Engineer',
                'description': 'We are looking for an experienced Full Stack Engineer to join our team. You will work on building scalable web applications using modern technologies.\n\nResponsibilities:\n- Design and develop full-stack web applications\n- Write clean, maintainable code\n- Collaborate with product and design teams\n- Mentor junior engineers\n\nRequirements:\n- 5+ years of experience with Python and JavaScript\n- Experience with React and Django\n- Strong understanding of databases and APIs\n- Excellent problem-solving skills',
                'location': 'Mountain View, CA',
                'latitude': 37.3861,
                'longitude': -122.0839,
                'salary_min': 150000,
                'salary_max': 220000,
                'is_remote': False,
                'visa_sponsorship': True,
                'company_name': 'Google',
                'company_logo': 'https://logo.clearbit.com/google.com',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'required_skills': 'Python, Django, React, JavaScript, PostgreSQL, AWS',
                'posted_by': google_recruiter,
                'is_active': True,
            },
            {
                'title': 'Data Scientist - Machine Learning',
                'description': 'Join our AI team to build cutting-edge machine learning models for search and recommendations.\n\nWhat you\'ll do:\n- Develop ML models for personalization\n- Analyze large datasets\n- Collaborate with engineering teams\n- Present findings to leadership\n\nQualifications:\n- MS/PhD in Computer Science or related field\n- Strong Python and ML framework experience\n- Experience with TensorFlow or PyTorch\n- Published research is a plus',
                'location': 'San Francisco, CA',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'salary_min': 160000,
                'salary_max': 250000,
                'is_remote': False,
                'visa_sponsorship': True,
                'company_name': 'Google',
                'company_logo': 'https://logo.clearbit.com/google.com',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'required_skills': 'Python, Machine Learning, TensorFlow, PyTorch, Statistics, Data Analysis',
                'posted_by': google_recruiter,
                'is_active': True,
            },
            {
                'title': 'Frontend Developer',
                'description': 'We need a talented Frontend Developer to create amazing user experiences.\n\nKey Responsibilities:\n- Build responsive web interfaces\n- Implement designs with pixel-perfect accuracy\n- Optimize for performance\n- Work with designers and backend engineers\n\nRequirements:\n- 3+ years of JavaScript experience\n- Expert in React or Vue.js\n- Strong CSS and HTML skills\n- Portfolio required',
                'location': 'Remote',
                'salary_min': 120000,
                'salary_max': 180000,
                'is_remote': True,
                'visa_sponsorship': False,
                'company_name': 'Google',
                'company_logo': 'https://logo.clearbit.com/google.com',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'required_skills': 'JavaScript, React, Vue.js, CSS, HTML, TypeScript',
                'posted_by': google_recruiter,
                'is_active': True,
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Looking for a DevOps Engineer to manage our cloud infrastructure and CI/CD pipelines.\n\nResponsibilities:\n- Manage AWS infrastructure\n- Build and maintain CI/CD pipelines\n- Monitor system performance\n- Implement security best practices\n\nRequirements:\n- 4+ years of DevOps experience\n- Strong AWS knowledge\n- Experience with Docker and Kubernetes\n- Infrastructure as Code (Terraform)',
                'location': 'Seattle, WA',
                'latitude': 47.6062,
                'longitude': -122.3321,
                'salary_min': 140000,
                'salary_max': 200000,
                'is_remote': False,
                'visa_sponsorship': True,
                'company_name': 'Amazon',
                'company_logo': 'https://logo.clearbit.com/amazon.com',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'required_skills': 'AWS, Docker, Kubernetes, Terraform, Jenkins, Linux, Python',
                'posted_by': amazon_recruiter,
                'is_active': True,
            },
            {
                'title': 'Software Development Engineer',
                'description': 'Join Amazon as an SDE and work on systems that impact millions of customers.\n\nWhat you will do:\n- Design and develop scalable systems\n- Write high-quality code\n- Participate in code reviews\n- On-call rotation\n\nQualifications:\n- BS in Computer Science or equivalent\n- 2+ years of programming experience\n- Proficiency in Java, C++, or Python\n- Strong algorithms and data structures knowledge',
                'location': 'Austin, TX',
                'latitude': 30.2672,
                'longitude': -97.7431,
                'salary_min': 130000,
                'salary_max': 190000,
                'is_remote': False,
                'visa_sponsorship': True,
                'company_name': 'Amazon',
                'company_logo': 'https://logo.clearbit.com/amazon.com',
                'job_type': 'full_time',
                'experience_level': 'entry',
                'required_skills': 'Java, Python, C++, Algorithms, Data Structures, System Design',
                'posted_by': amazon_recruiter,
                'is_active': True,
            },
            {
                'title': 'Backend Engineer - Fintech',
                'description': 'Exciting opportunity at a fast-growing fintech startup!\n\nRole:\n- Build payment processing systems\n- Develop RESTful APIs\n- Ensure system security and compliance\n- Work in an agile environment\n\nRequirements:\n- 3+ years backend development\n- Experience with microservices\n- Knowledge of payment systems (preferred)\n- Startup mentality',
                'location': 'Atlanta, GA',
                'latitude': 33.7490,
                'longitude': -84.3880,
                'salary_min': 110000,
                'salary_max': 150000,
                'is_remote': True,
                'visa_sponsorship': False,
                'company_name': 'TechFlow Solutions',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'required_skills': 'Java, Spring Boot, Microservices, REST APIs, PostgreSQL, Redis',
                'posted_by': startup_recruiter,
                'is_active': True,
            },
            {
                'title': 'Product Manager - Mobile',
                'description': 'Lead product development for our mobile applications.\n\nResponsibilities:\n- Define product roadmap\n- Work with engineering and design\n- Analyze user metrics\n- Launch new features\n\nQualifications:\n- 4+ years of product management\n- Experience with mobile apps\n- Strong analytical skills\n- MBA preferred',
                'location': 'San Francisco, CA',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'salary_min': 140000,
                'salary_max': 180000,
                'is_remote': False,
                'visa_sponsorship': False,
                'company_name': 'TechFlow Solutions',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'required_skills': 'Product Management, Agile, Analytics, Mobile, SQL, User Research',
                'posted_by': startup_recruiter,
                'is_active': True,
            },
            {
                'title': 'iOS Developer',
                'description': 'Build amazing iOS experiences for our users.\n\nWhat you\'ll do:\n- Develop iOS applications\n- Implement new features\n- Fix bugs and optimize performance\n- Collaborate with designers\n\nRequirements:\n- 3+ years iOS development\n- Swift expertise\n- App Store published apps\n- UI/UX sensibility',
                'location': 'Los Angeles, CA',
                'latitude': 34.0522,
                'longitude': -118.2437,
                'salary_min': 120000,
                'salary_max': 170000,
                'is_remote': True,
                'visa_sponsorship': True,
                'company_name': 'Amazon',
                'company_logo': 'https://logo.clearbit.com/amazon.com',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'required_skills': 'Swift, iOS Development, UIKit, SwiftUI, Core Data, Firebase',
                'posted_by': amazon_recruiter,
                'is_active': True,
            },
            {
                'title': 'Security Engineer',
                'description': 'Protect our infrastructure and customer data.\n\nKey Duties:\n- Security assessments and audits\n- Incident response\n- Implement security controls\n- Security training\n\nRequirements:\n- 5+ years security experience\n- CISSP or similar certification\n- Penetration testing skills\n- Cloud security knowledge',
                'location': 'Washington, DC',
                'latitude': 38.9072,
                'longitude': -77.0369,
                'salary_min': 150000,
                'salary_max': 210000,
                'is_remote': False,
                'visa_sponsorship': True,
                'company_name': 'Google',
                'company_logo': 'https://logo.clearbit.com/google.com',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'required_skills': 'Cybersecurity, Penetration Testing, SIEM, Network Security, Python, Cloud Security',
                'posted_by': google_recruiter,
                'is_active': True,
            },
            {
                'title': 'Junior Software Engineer',
                'description': 'Perfect for new graduates! Join our engineering team.\n\nYou will:\n- Write code for web applications\n- Learn from senior engineers\n- Participate in code reviews\n- Contribute to projects\n\nQualifications:\n- BS in Computer Science (or graduating soon)\n- Internship experience preferred\n- Knowledge of Python or Java\n- Passion for learning',
                'location': 'Atlanta, GA',
                'latitude': 33.7490,
                'longitude': -84.3880,
                'salary_min': 80000,
                'salary_max': 110000,
                'is_remote': False,
                'visa_sponsorship': True,
                'company_name': 'TechFlow Solutions',
                'job_type': 'full_time',
                'experience_level': 'entry',
                'required_skills': 'Python, Java, JavaScript, Git, SQL, Problem Solving',
                'posted_by': startup_recruiter,
                'is_active': True,
            },
        ]

        for job_data in jobs_data:
            Job.objects.create(**job_data)
            self.stdout.write(f'  [OK] Created job: {job_data["title"]} at {job_data["company_name"]}')

    def create_applications(self):
        """Create sample job applications"""
        self.stdout.write('Creating job applications...')

        # Get users
        alice = User.objects.get(username='demo_alice')
        bob = User.objects.get(username='demo_bob')
        carol = User.objects.get(username='demo_carol')
        david = User.objects.get(username='demo_david')
        emma = User.objects.get(username='demo_emma')
        frank = User.objects.get(username='demo_frank')
        grace = User.objects.get(username='demo_grace')
        henry = User.objects.get(username='demo_henry')

        # Get jobs
        jobs = list(Job.objects.all())

        applications_data = [
            # Alice applies to multiple jobs
            {'user': alice, 'job': jobs[0], 'status': 'interview', 'note': 'Very excited about this opportunity! I have extensive experience with Django and React.'},
            {'user': alice, 'job': jobs[2], 'status': 'reviewed', 'note': 'My portfolio showcases 5+ React projects.'},
            {'user': alice, 'job': jobs[5], 'status': 'applied', 'note': 'Interested in the fintech space and backend development.'},

            # Bob applies to data science roles
            {'user': bob, 'job': jobs[1], 'status': 'interview', 'note': 'PhD candidate with 2 published ML papers. Would love to discuss my research.'},
            {'user': bob, 'job': jobs[4], 'status': 'applied', 'note': 'Strong algorithms background from MIT.'},

            # Carol applies to frontend roles
            {'user': carol, 'job': jobs[2], 'status': 'accepted', 'note': 'See my portfolio at carol.design - I specialize in accessibility and performance.'},
            {'user': carol, 'job': jobs[0], 'status': 'reviewed', 'note': 'Full stack experience with emphasis on frontend.'},

            # David applies to DevOps roles
            {'user': david, 'job': jobs[3], 'status': 'interview', 'note': 'Managed AWS infrastructure serving 10M users. Terraform expert.'},
            {'user': david, 'job': jobs[5], 'status': 'applied', 'note': 'Interested in building fintech infrastructure.'},

            # Emma applies to PM roles
            {'user': emma, 'job': jobs[6], 'status': 'interview', 'note': 'MBA from UW. Launched 3 mobile products at Microsoft.'},

            # Frank applies to backend roles
            {'user': frank, 'job': jobs[5], 'status': 'reviewed', 'note': 'Built microservices handling 1M+ transactions daily at Stripe.'},
            {'user': frank, 'job': jobs[4], 'status': 'applied', 'note': 'Strong Java and system design background.'},

            # Grace applies to mobile roles
            {'user': grace, 'job': jobs[7], 'status': 'accepted', 'note': 'Published 3 iOS apps with 4.8+ ratings. Portfolio available on request.'},
            {'user': grace, 'job': jobs[6], 'status': 'rejected', 'note': 'Would love to transition to PM from engineering.'},

            # Henry applies to security roles
            {'user': henry, 'job': jobs[8], 'status': 'interview', 'note': 'CMU Information Security MS. CISSP certified. Reduced vulnerabilities by 60% at Cloudflare.'},
        ]

        for app_data in applications_data:
            app = JobApplication.objects.create(**app_data)
            self.stdout.write(f'  [OK] Created application: {app_data["user"].username} -> {app_data["job"].title}')

    def create_messages(self):
        """Create sample messages between recruiters and candidates"""
        self.stdout.write('Creating messages...')

        google_recruiter = User.objects.get(username='demo_recruiter_google')
        alice = User.objects.get(username='demo_alice')
        bob = User.objects.get(username='demo_bob')
        henry = User.objects.get(username='demo_henry')

        messages_data = [
            {
                'sender': google_recruiter,
                'recipient': alice,
                'subject': 'Interview Invitation - Senior Full Stack Engineer',
                'body': 'Hi Alice,\n\nThank you for applying to our Senior Full Stack Engineer position. We were impressed by your background and would like to invite you for a technical interview.\n\nWould you be available next Tuesday or Wednesday afternoon?\n\nBest regards,\nSarah Thompson\nTechnical Recruiter, Google',
                'is_read': True,
            },
            {
                'sender': alice,
                'recipient': google_recruiter,
                'subject': 'Re: Interview Invitation - Senior Full Stack Engineer',
                'body': 'Hi Sarah,\n\nThank you so much for the opportunity! I would be available on Wednesday afternoon. What time works best for your team?\n\nLooking forward to speaking with you.\n\nBest,\nAlice Johnson',
                'is_read': False,
            },
            {
                'sender': google_recruiter,
                'recipient': bob,
                'subject': 'Next Steps - Data Scientist Position',
                'body': 'Hi Bob,\n\nCongratulations! You have advanced to the next round of interviews for the Data Scientist - Machine Learning position.\n\nWe would like to schedule a virtual onsite interview with 4 team members. This will take approximately 3-4 hours. Are you available next week?\n\nBest,\nSarah',
                'is_read': True,
            },
            {
                'sender': google_recruiter,
                'recipient': henry,
                'subject': 'Security Engineer Opportunity',
                'body': 'Hi Henry,\n\nI came across your profile and was impressed by your security background at Cloudflare. We have a Security Engineer position that would be perfect for someone with your expertise.\n\nWould you be interested in learning more about this opportunity?\n\nBest regards,\nSarah Thompson\nGoogle',
                'is_read': False,
            },
        ]

        for msg_data in messages_data:
            Message.objects.create(**msg_data)
            self.stdout.write(f'  [OK] Created message: {msg_data["sender"].username} -> {msg_data["recipient"].username}')

    def print_summary(self):
        """Print summary of created data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('DATABASE SEEDING SUMMARY'))
        self.stdout.write('='*50 + '\n')

        self.stdout.write(f'Job Seekers: {User.objects.filter(profile__user_type="job_seeker", username__startswith="demo_").count()}')
        self.stdout.write(f'Recruiters: {User.objects.filter(profile__user_type="recruiter", username__startswith="demo_").count()}')
        self.stdout.write(f'Education Entries: {Education.objects.filter(profile__user__username__startswith="demo_").count()}')
        self.stdout.write(f'Work Experience Entries: {WorkExperience.objects.filter(profile__user__username__startswith="demo_").count()}')
        self.stdout.write(f'Job Postings: {Job.objects.filter(posted_by__username__startswith="demo_").count()}')
        self.stdout.write(f'Applications: {JobApplication.objects.filter(user__username__startswith="demo_").count()}')
        self.stdout.write(f'Messages: {Message.objects.filter(sender__username__startswith="demo_").count()}')

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('TEST ACCOUNTS'))
        self.stdout.write('='*50 + '\n')

        self.stdout.write('JOB SEEKERS (all password: password123):')
        self.stdout.write('  • demo_alice (Full Stack Dev - Atlanta)')
        self.stdout.write('  • demo_bob (Data Scientist - SF)')
        self.stdout.write('  • demo_carol (Frontend Dev - NYC)')
        self.stdout.write('  • demo_david (DevOps - Austin)')
        self.stdout.write('  • demo_emma (Product Manager - Seattle)')
        self.stdout.write('  • demo_frank (Backend Engineer - Boston)')
        self.stdout.write('  • demo_grace (Mobile Dev - LA)')
        self.stdout.write('  • demo_henry (Security - DC)')

        self.stdout.write('\nRECRUITERS (all password: password123):')
        self.stdout.write('  • demo_recruiter_google (Google)')
        self.stdout.write('  • demo_recruiter_amazon (Amazon)')
        self.stdout.write('  • demo_recruiter_startup (TechFlow Solutions)')

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('[SUCCESS] Ready to test all user stories!'))
        self.stdout.write('='*50 + '\n')
