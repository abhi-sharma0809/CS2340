# Deploy to PythonAnywhere - Complete Guide

This guide covers deploying the GT Job Finder application to PythonAnywhere.

## Initial Setup (First Time Deployment)

### 1. Create PythonAnywhere Account
- Sign up at https://www.pythonanywhere.com
- Choose a username (this will be part of your URL: `username.pythonanywhere.com`)

### 2. Clone Your Repository

In the PythonAnywhere Bash console:
```bash
cd ~
git clone https://github.com/yourusername/CS2340.git
cd CS2340
```

### 3. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.12 jobfindervirtualenv
workon jobfindervirtualenv
pip install -r requirements.txt
```

### 4. Set Up the Web App

1. Go to the **Web** tab in PythonAnywhere
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Django)
4. Choose **Python 3.12**

### 5. Configure WSGI File

Click on the WSGI configuration file link and replace its contents with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOURUSERNAME/CS2340'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'gtjobfinder.settings'

# Activate your virtual environment
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: Replace `YOURUSERNAME` with your actual PythonAnywhere username!

### 6. Configure Static Files

In the **Web** tab, add these static file mappings:

| URL          | Directory                                    |
|--------------|---------------------------------------------|
| /static/     | /home/YOURUSERNAME/CS2340/static           |

### 7. Update Settings for Production

Edit `gtjobfinder/settings.py` and add your PythonAnywhere domain:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', 'YOURUSERNAME.pythonanywhere.com']
```

Commit and push this change to GitHub.

### 8. Run Migrations

```bash
cd ~/CS2340
workon jobfindervirtualenv
python manage.py migrate
```

### 9. Create Admin User

**Critical Step** - The database is not pushed to Git, so you need to create an admin:

```bash
python manage.py createsuperuser
```

Or promote an existing user after they sign up:
```bash
python manage.py make_admin username
```

### 10. Reload Your Web App

Go to the **Web** tab and click the big green **Reload** button.

Your app should now be live at `https://YOURUSERNAME.pythonanywhere.com`!

---

## Updating Your Deployed App (After Changes)

When you've made changes and want to deploy them:

### 1. Push Changes from Local Machine

```bash
git add .
git commit -m "Your descriptive commit message"
git push origin main
```

### 2. Pull Changes on PythonAnywhere

In the PythonAnywhere Bash console:
```bash
cd ~/CS2340
git pull origin main
```

### 3. Activate Virtual Environment

```bash
workon jobfindervirtualenv
```

### 4. Run Any New Migrations

**Always run this after pulling changes:**
```bash
python manage.py migrate
```

If you added migrations to specific apps:
```bash
python manage.py migrate accounts
python manage.py migrate jobs
```

### 5. Collect Static Files (if CSS/JS changed)

```bash
python manage.py collectstatic --noinput
```

### 6. Reload Your Web App

Go to the **Web** tab and click the **Reload** button.

---

## Quick Deploy Command Sequence

```bash
cd ~/CS2340
git pull origin main
workon jobfindervirtualenv
python manage.py migrate
python manage.py collectstatic --noinput
# Go to Web tab and click Reload
```

---

## Important Migrations to Run

The app has several critical migrations that must be applied:

### Profile Location Fix
```bash
python manage.py migrate accounts
```

This includes migration `0006_alter_profile_location` which:
- Sets default location for job seekers to `''` (empty string)
- Sets location for recruiters to `'N/A - Recruiter'`
- Fixes `NOT NULL` constraint errors during signup

### Job Model Updates
```bash
python manage.py migrate jobs
```

This includes migrations for:
- `is_active` field for job visibility
- `posted_by` to track which recruiter posted a job
- `ApplicationStatusHistory` model for tracking status changes
- `required_skills`, `job_type`, `experience_level` fields

---

## Troubleshooting

### Error: "NOT NULL constraint failed: accounts_profile.location"

**Solution**: Run the location migration:
```bash
cd ~/CS2340
workon jobfindervirtualenv
python manage.py migrate accounts
```

Check if it ran:
```bash
python manage.py showmigrations accounts
```

You should see `[X]` next to `0006_alter_profile_location`.

### Error: "DisallowedHost at /"

**Solution**: Add your domain to `ALLOWED_HOSTS` in `settings.py`:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'YOURUSERNAME.pythonanywhere.com']
```

### Static Files Not Loading (CSS/JS missing)

**Solution**:
1. Check static file mappings in the Web tab
2. Run `python manage.py collectstatic`
3. Reload the web app

### Database Errors After Migration

**Solution**: Check migration status:
```bash
python manage.py showmigrations
```

If migrations are missing `[X]`, run:
```bash
python manage.py migrate
```

### Email Not Sending

The app is configured to use Gmail SMTP. If emails aren't sending:
1. Check `gtjobfinder/settings.py` has correct Gmail credentials
2. Ensure you're using an App Password, not your regular Gmail password
3. For testing, you can switch to console backend:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

---

## Scheduled Tasks (Optional)

For the saved search notification feature, set up a scheduled task:

1. Go to the **Tasks** tab in PythonAnywhere
2. Add a new daily scheduled task:
   ```bash
   cd ~/CS2340 && /home/YOURUSERNAME/.virtualenvs/jobfindervirtualenv/bin/python manage.py check_saved_searches
   ```
3. Set it to run daily (e.g., 9:00 AM)

This will check for new candidates matching recruiters' saved searches and send notifications.

---

## Production Checklist

Before going live, make sure:

- ✅ `ALLOWED_HOSTS` includes your domain
- ✅ All migrations have been run (`python manage.py showmigrations`)
- ✅ Admin user has been created
- ✅ Static files are collected
- ✅ Web app has been reloaded
- ✅ Test all major features (signup, login, job search, applications)
- ✅ Test email sending (if using Gmail, ensure App Password is set)
- ✅ For production: Set `DEBUG = False` in settings (and configure error logging)

---

## Getting Help

If you encounter issues:

1. **Check the error log**: In the Web tab, click on the "Error log" link
2. **Check the server log**: In the Web tab, click on the "Server log" link
3. **Test in Django shell**:
   ```bash
   cd ~/CS2340
   workon jobfindervirtualenv
   python manage.py shell
   ```
4. **Verify database state**:
   ```bash
   python manage.py dbshell
   .tables
   .quit
   ```

---

## Environment Variables (Advanced)

For better security in production, consider using environment variables:

1. Create a `.env` file (add it to `.gitignore`)
2. Use `python-decouple` or similar to load variables
3. Store sensitive data (SECRET_KEY, EMAIL_PASSWORD, API_KEYS) in environment variables

This prevents accidentally committing credentials to Git.

---

**That's it!** 🎉 Your GT Job Finder app should now be deployed and accessible to the world.

For local development instructions, see the main [README.md](README.md).
For admin panel documentation, see [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md).
