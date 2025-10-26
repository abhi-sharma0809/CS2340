from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from jobs.models import SavedSearch, SearchNotification
from accounts.models import Profile
import re

User = get_user_model()


class Command(BaseCommand):
    help = 'Check saved searches for new candidate matches and send notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually sending notifications',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No notifications will be sent'))
        
        # Get all active saved searches with notifications enabled
        saved_searches = SavedSearch.objects.filter(
            notify_on_new_matches=True
        )
        
        total_notifications = 0
        
        for search in saved_searches:
            self.stdout.write(f'Checking search: {search.name}')
            
            # Find new matches since last notification
            new_matches = self.find_new_matches(search)
            
            if new_matches:
                self.stdout.write(f'  Found {len(new_matches)} new matches')
                
                if not dry_run:
                    # Create notification records
                    for candidate in new_matches:
                        SearchNotification.objects.get_or_create(
                            saved_search=search,
                            candidate=candidate
                        )
                    
                    # Update last notified timestamp
                    search.last_notified = timezone.now()
                    search.save()
                
                total_notifications += len(new_matches)
            else:
                self.stdout.write('  No new matches found')
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'Would send {total_notifications} notifications')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Sent {total_notifications} notifications')
            )

    def find_new_matches(self, search):
        """Find new candidate matches for a saved search"""
        # Get job seekers
        job_seekers = User.objects.filter(
            profile__user_type='job_seeker',
            profile__is_public=True
        ).select_related('profile')
        
        new_matches = []
        
        for user in job_seekers:
            profile = user.profile
            
            # Check if this candidate matches the search criteria
            if self.matches_search_criteria(profile, search):
                # Check if we've already notified about this candidate
                if not SearchNotification.objects.filter(
                    saved_search=search,
                    candidate=user
                ).exists():
                    new_matches.append(user)
        
        return new_matches

    def matches_search_criteria(self, profile, search):
        """Check if a profile matches the search criteria"""
        match_score = 0
        
        # Skills matching
        if search.skills:
            user_skills = self._skill_tokens(profile.skills or '')
            search_skills = self._skill_tokens(search.skills)
            skill_matches = len(set(user_skills) & set(search_skills))
            if skill_matches > 0:
                match_score += skill_matches * 10
        
        # Education matching
        if search.education_keywords and profile.education:
            education_lower = profile.education.lower()
            education_keywords = search.education_keywords.lower().split()
            education_matches = sum(1 for keyword in education_keywords if keyword in education_lower)
            if education_matches > 0:
                match_score += education_matches * 5
        
        # Experience matching
        if search.experience_keywords and profile.experience:
            experience_lower = profile.experience.lower()
            experience_keywords = search.experience_keywords.lower().split()
            experience_matches = sum(1 for keyword in experience_keywords if keyword in experience_lower)
            if experience_matches > 0:
                match_score += experience_matches * 5
        
        # Location matching (simplified)
        if search.location and profile.commute_radius_km:
            # This is a simplified location match
            if search.location.lower() in (profile.user.email.split('@')[1] if '@' in profile.user.email else ''):
                match_score += 3
        
        # Return True if there's any match
        return match_score > 0

    def _skill_tokens(self, text):
        """Extract skill tokens from text"""
        if not text:
            return []
        # Split on commas/newlines and non-alphanumerics; lower-case; dedupe
        raw = re.split(r"[,\n]+", text)
        tokens = []
        for chunk in raw:
            for t in re.findall(r"[A-Za-z0-9+#\.]+", chunk.lower()):
                if len(t) >= 2:
                    tokens.append(t)
        return list(dict.fromkeys(tokens))  # preserve order, remove dups
