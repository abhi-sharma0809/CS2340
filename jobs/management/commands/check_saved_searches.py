"""
Management command to check saved searches for new candidate matches
and notify recruiters.

Run this command periodically (e.g., via cron job):
    python manage.py check_saved_searches
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from jobs.models import SavedSearch, SearchNotification
from accounts.models import Profile, Message

User = get_user_model()


class Command(BaseCommand):
    help = 'Check saved searches for new candidate matches and notify recruiters'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Only check profiles updated in the last N hours (default: 24)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without actually sending notifications'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No notifications will be sent'))
        
        # Get all saved searches with notifications enabled
        saved_searches = SavedSearch.objects.filter(notify_on_new_matches=True)
        
        self.stdout.write(f'Checking {saved_searches.count()} saved searches...')
        
        total_notifications = 0
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        for search in saved_searches:
            notifications_sent = self._check_search(search, cutoff_time, dry_run)
            total_notifications += notifications_sent
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'DRY RUN: Would have sent {total_notifications} notifications'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully sent {total_notifications} notifications'
            ))

    def _check_search(self, search, cutoff_time, dry_run):
        """Check a single saved search for new matches"""
        notifications_sent = 0
        
        # Get job seekers who match the search criteria
        job_seekers = User.objects.filter(
            profile__user_type='job_seeker',
            profile__is_public=True
        ).select_related('profile')
        
        # Only check recently updated profiles
        # Filter by user's last_login as a proxy for profile updates
        # In production, you'd want a last_updated field on Profile
        if search.last_notified:
            job_seekers = job_seekers.filter(
                last_login__gte=search.last_notified
            )
        
        for user in job_seekers:
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                continue
            
            # Check if we've already notified about this candidate
            if SearchNotification.objects.filter(
                saved_search=search,
                candidate=user
            ).exists():
                continue
            
            # Calculate match score
            match_score = self._calculate_match_score(profile, search)
            
            if match_score > 0:
                # Send notification
                if not dry_run:
                    self._send_notification(search, user, profile, match_score)
                    
                    # Create notification record
                    SearchNotification.objects.create(
                        saved_search=search,
                        candidate=user
                    )
                
                notifications_sent += 1
                self.stdout.write(
                    f'  ✓ New match: {user.username} (score: {match_score}) '
                    f'for search "{search.name}"'
                )
        
        # Update last_notified timestamp
        if not dry_run and notifications_sent > 0:
            search.last_notified = timezone.now()
            search.save()
        
        return notifications_sent

    def _calculate_match_score(self, profile, search):
        """Calculate how well a profile matches a saved search"""
        match_score = 0
        
        # Skills matching
        if search.skills and profile.skills:
            try:
                from jobs.views import _skill_tokens
                user_skills = set(_skill_tokens(profile.skills))
                search_skills = set(_skill_tokens(search.skills))
                skill_matches = len(user_skills & search_skills)
                match_score += skill_matches * 10
            except Exception:
                pass
        
        # Education matching
        if search.education_keywords and profile.education:
            education_lower = profile.education.lower()
            education_keywords = search.education_keywords.lower().split()
            matches = sum(1 for keyword in education_keywords if keyword in education_lower)
            match_score += matches * 5
        
        # Experience matching
        if search.experience_keywords and profile.experience:
            experience_lower = profile.experience.lower()
            experience_keywords = search.experience_keywords.lower().split()
            matches = sum(1 for keyword in experience_keywords if keyword in experience_lower)
            match_score += matches * 5
        
        # Location matching
        if search.location and profile.location:
            location_lower = search.location.lower()
            profile_location_lower = profile.location.lower()
            
            if (location_lower in profile_location_lower or 
                profile_location_lower in location_lower or
                any(word in profile_location_lower for word in location_lower.split(','))):
                match_score += 5
        
        return match_score

    def _send_notification(self, search, user, profile, match_score):
        """Send a notification message to the recruiter about the new match"""
        
        # Build match details
        match_details = []
        if profile.skills:
            match_details.append(f"Skills: {profile.skills[:100]}")
        if profile.location:
            match_details.append(f"Location: {profile.location}")
        if profile.education:
            match_details.append(f"Education: {profile.education[:100]}")
        
        details_text = '\n'.join(f"• {detail}" for detail in match_details[:3])
        
        subject = f'New candidate match for "{search.name}"'
        body = f'''A new candidate matches your saved search "{search.name}"!

Candidate: {user.get_full_name() or user.username}
Match Score: {match_score} points

{details_text}

View their full profile to learn more about them.
'''
        
        # Create in-platform message
        Message.objects.create(
            sender=User.objects.filter(is_superuser=True).first() or search.recruiter,
            recipient=search.recruiter,
            subject=subject,
            body=body
        )
