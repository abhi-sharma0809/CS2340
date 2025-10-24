# Outlook/Hotmail Email Setup for GT Job Finder

## 🚀 Super Simple Setup (No App Passwords!)

### Step 1: Use Your Outlook/Hotmail Account

You can use any of these email providers:
- **@outlook.com**
- **@hotmail.com**
- **@live.com**

Just use your regular password - no special app passwords needed!

### Step 2: Update Django Settings

Open `gtjobfinder/settings.py` and update lines 139, 143, and 144:

```python
DEFAULT_FROM_EMAIL = 'your-email@outlook.com'
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-regular-password'
```

### Step 3: Restart Server

Stop the Django server (Ctrl+C) and restart it:
```bash
python3 manage.py runserver
```

### Step 4: Test It!

Run this command:
```bash
python3 manage.py shell -c "
from django.core.mail import send_mail
send_mail(
    'Test from GT Job Finder',
    'It works!',
    'your-email@outlook.com',
    ['your-email@outlook.com'],
)
print('✅ Email sent!')
"
```

---

## ✅ Advantages of Outlook over Gmail

- ✅ **No 2-Factor Authentication required**
- ✅ **No app passwords needed**
- ✅ **Just use your regular password**
- ✅ **Works instantly**
- ✅ **Higher daily sending limits**

---

## 🎯 Quick Example

If your email is `john@outlook.com` and password is `MyPassword123`:

```python
DEFAULT_FROM_EMAIL = 'john@outlook.com'
EMAIL_HOST_USER = 'john@outlook.com'
EMAIL_HOST_PASSWORD = 'MyPassword123'
```

That's it! No special setup required.

---

## 🔒 Security Note

Your password is stored in `settings.py`. For better security:
1. Add `settings.py` to `.gitignore` (already done)
2. Use environment variables for production
3. Never commit passwords to git

---

## ✨ You're All Set!

Once you add your Outlook credentials:
- Send emails from recruiter dashboard ✓
- Email candidates about jobs ✓
- Real emails delivered to inboxes ✓
- No more console output ✓

