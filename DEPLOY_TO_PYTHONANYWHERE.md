# Deploy to PythonAnywhere - Fix Location Field Error

## Steps to Deploy the Fix

### 1. Upload the Updated Code

From your local machine, push to GitHub:
```bash
git add .
git commit -m "Fix location field NOT NULL constraint error"
git push origin main
```

### 2. Pull on PythonAnywhere

In the PythonAnywhere Bash console:
```bash
cd ~/CS2340
git pull origin main
```

### 3. Run the Migration

This is **CRITICAL** - run the new migration that fixes the database:
```bash
cd ~/CS2340
python manage.py migrate accounts
```

You should see:
```
Applying accounts.0006_alter_profile_location... OK
```

### 4. Reload Your Web App

In the PythonAnywhere Web tab:
- Click the **"Reload"** button for your web app
- Wait for it to finish reloading

### 5. Test

Try creating a new recruiter account - it should work now!

---

## What This Migration Does

The migration (`0006_alter_profile_location.py`) does three things:

1. **Updates existing recruiter profiles** - Sets location to `'N/A - Recruiter'` for any NULL locations where user_type is 'recruiter'
2. **Updates existing job seeker profiles** - Sets location to `''` (empty string) for any NULL locations where user_type is 'job_seeker'  
3. **Alters the field** - Adds `default=''` to the location field, so new profiles will always have at least an empty string

This ensures:
- ✅ No more NOT NULL constraint errors
- ✅ All existing profiles are fixed
- ✅ All new profiles (both recruiters and job seekers) will work
- ✅ The database schema matches the model definition

---

## If You Still Get Errors

If you still see the error after following these steps:

### Check the migration ran:
```bash
python manage.py showmigrations accounts
```

You should see:
```
[X] 0001_initial
[X] 0002_...
[X] 0003_...
[X] 0004_...
[X] 0005_profile_latitude_profile_location_profile_longitude
[X] 0006_alter_profile_location  ← This should have an [X]
```

### Manually fix the database (last resort):
```bash
python manage.py shell
```

Then run:
```python
from accounts.models import Profile

# Fix all profiles with NULL location
Profile.objects.filter(location__isnull=True, user_type='recruiter').update(location='N/A - Recruiter')
Profile.objects.filter(location__isnull=True, user_type='job_seeker').update(location='')
Profile.objects.filter(location='').count()  # Should show number of profiles fixed

exit()
```

### Verify the schema:
```bash
python manage.py dbshell
```

Then:
```sql
PRAGMA table_info(accounts_profile);
```

Look for the `location` field - it should show:
- `dflt_value` column should have a value ('' or NULL is ok)
- `notnull` should be 0 (meaning it ALLOWS null)

Type `.quit` to exit.

---

## Quick Reference

**Complete deployment command sequence:**
```bash
cd ~/CS2340
git pull origin main
python manage.py migrate accounts
# Go to Web tab and click Reload
```

That's it! 🎉

