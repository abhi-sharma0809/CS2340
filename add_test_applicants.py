#!/usr/bin/env python
"""Script to add test applicants to a Google recruiter job"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gtjobfinder.settings')
django.setup()

from django.contrib.auth.models import User
from jobs.models import Job, JobApplication
from datetime import datetime, timedelta
import random

def main():
    # Get Google recruiter
    try:
        google_recruiter = User.objects.get(username='demo_recruiter_google')
    except User.DoesNotExist:
        print('ERROR: demo_recruiter_google not found')
        return

    # Get one of their jobs
    job = Job.objects.filter(posted_by=google_recruiter).first()
    if not job:
        print('ERROR: No jobs found for demo_recruiter_google')
        return

    print(f'Adding applicants to: {job.title}')
    print(f'Job ID: {job.id}')
    print('-' * 60)

    # Get all demo job seekers
    job_seekers = User.objects.filter(
        username__startswith='demo_',
        profile__user_type='job_seeker'
    ).select_related('profile')

    print(f'Found {job_seekers.count()} demo job seekers')

    # Application statuses for variety
    statuses = ['applied', 'reviewed', 'interview', 'applied', 'reviewed', 'applied', 'applied', 'interview']

    # Create applications
    created_count = 0
    for i, seeker in enumerate(job_seekers):
        # Check if already applied
        existing = JobApplication.objects.filter(job=job, user=seeker).exists()
        if existing:
            print(f'  - {seeker.username} already applied, skipping')
            continue

        # Create application
        status = statuses[i % len(statuses)]

        try:
            application = JobApplication.objects.create(
                job=job,
                user=seeker,
                status=status,
                note=f'I am very interested in the {job.title} position. I believe my skills in {seeker.profile.skills[:50] if seeker.profile.skills else "various technologies"} make me a great fit for this role at {job.company_name}.'
            )
            created_count += 1
            name = seeker.get_full_name() or seeker.username
            location = seeker.profile.location if hasattr(seeker, 'profile') and seeker.profile.location else 'Unknown'
            print(f'  [OK] {name} ({location}) - Status: {status}')
        except Exception as e:
            print(f'  [ERROR] Failed to create application for {seeker.username}: {e}')

    print('-' * 60)
    print(f'Total applications created: {created_count}')
    print(f'Job now has {JobApplication.objects.filter(job=job).count()} total applicants')
    print()
    print(f'View applicants map at:')
    print(f'http://127.0.0.1:8000/jobs/{job.id}/applicants-map/')
    print()
    print(f'View applicants list at:')
    print(f'http://127.0.0.1:8000/jobs/{job.id}/applicants/')

if __name__ == '__main__':
    main()
