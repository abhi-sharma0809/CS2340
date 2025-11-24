# Saved Search Notifications

## Overview
Recruiters can save candidate searches and receive automatic notifications when new candidates match their criteria.

## How It Works

### For Recruiters

1. **Create a Saved Search**:
   - Go to "Candidate Search" in the recruiter dashboard
   - Enter your search criteria (skills, location, education, experience)
   - Click "Save This Search"
   - Give it a name and description
   - **Enable "Notify me about new matches"** checkbox

2. **Manual Check** (Testing):
   - Go to "Saved Searches" page
   - Click the **"Check for New Matches"** button
   - The system will immediately scan all job seekers and send you messages about new matches

3. **Automatic Notifications** (Production):
   - Set up a cron job or scheduled task to run:
     ```bash
     python manage.py check_saved_searches
     ```
   - Recommended frequency: Once per day (e.g., 9 AM)
   - Example cron job (runs daily at 9 AM):
     ```
     0 9 * * * cd /path/to/project && python manage.py check_saved_searches
     ```

4. **Viewing Notifications**:
   - Click the "Notifications" button on the Saved Searches page
   - Or check your "Messages" tab - new matches appear as messages
   - Each message includes:
     - Candidate name
     - Match score
     - Preview of their skills, location, and education
     - Link to view their full profile

## Management Command Options

```bash
# Check saved searches (default: last 24 hours)
python manage.py check_saved_searches

# Check only profiles updated in last 48 hours
python manage.py check_saved_searches --hours 48

# Dry run (see what would happen without sending notifications)
python manage.py check_saved_searches --dry-run
```

## Match Scoring

The system calculates a match score based on:
- **Skills**: 10 points per matching skill
- **Education**: 5 points per matching keyword
- **Experience**: 5 points per matching keyword
- **Location**: 5 points for location match

Higher scores indicate better matches.

## Features

### Deduplication
- The system tracks which candidates you've already been notified about
- You won't receive duplicate notifications for the same candidate on the same saved search

### Last Notified Timestamp
- Each saved search tracks when it last sent notifications
- This helps focus on new or recently updated profiles

### In-Platform Messages
- All notifications appear as messages in your Messages tab
- You can reply to candidates directly from the message
- Messages include direct links to candidate profiles

## For Job Seekers

To appear in recruiter searches:
1. **Make sure your profile is public**
2. **Add your location** in Profile Edit
3. **Fill out your skills, education, and experience**
4. **Keep your profile updated** - recent updates may trigger notifications

## Technical Details

- Notifications are tracked in the `SearchNotification` model
- Saved search criteria are stored in the `SavedSearch` model
- Location matching uses text-based comparison (exact coordinates optional)
- The system is designed to be run daily but can be adjusted based on your needs

## Troubleshooting

**Not receiving notifications?**
- Check that "Notify on new matches" is enabled for your saved search
- Verify that candidates have public profiles with matching criteria
- Run `python manage.py check_saved_searches --dry-run` to see potential matches

**Too many notifications?**
- Make your search criteria more specific
- Adjust the frequency of the cron job
- Consider disabling notifications for less important searches

