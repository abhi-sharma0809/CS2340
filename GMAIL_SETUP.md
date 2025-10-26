# 📧 Gmail SMTP Setup Guide

## Quick Steps to Get Gmail Working

### Step 1: Enable 2-Factor Authentication (Required!)

1. Go to: https://myaccount.google.com/security
2. Under "Signing in to Google", click **"2-Step Verification"**
3. Follow the prompts to enable it (if not already enabled)

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
2. You might need to sign in again
3. Select:
   - **App**: Mail
   - **Device**: Other (Custom name) → Type "Django GT Job Finder"
4. Click **"Generate"**
5. You'll see a **16-character password** like: `abcd efgh ijkl mnop`

### Step 3: Update Django Settings

Open `gtjobfinder/settings.py` and update these 3 lines:

```python
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Line 142
EMAIL_HOST_USER = 'your-email@gmail.com'     # Line 146
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'     # Line 147 (NO SPACES!)
```

**Important:** 
- Remove ALL spaces from the app password
- Use the same Gmail address for both `DEFAULT_FROM_EMAIL` and `EMAIL_HOST_USER`

### Step 4: Test It!

```bash
cd /Users/joelagodio/PycharmProjects/CS2340
python3 manage.py shell -c "
from django.core.mail import send_mail
send_mail(
    'Test Email from GT Job Finder',
    'If you receive this, Gmail is working!',
    'your-email@gmail.com',
    ['your-email@gmail.com'],
)
print('✅ Email sent! Check your inbox.')
"
```

---

## Example Configuration

```python
# Real example (with fake credentials):
DEFAULT_FROM_EMAIL = 'jobfindercs@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jobfindercs@gmail.com'
EMAIL_HOST_PASSWORD = 'xyzabcdefghijklm'  # 16 chars, no spaces
```

---

## Troubleshooting

### "Username and Password not accepted"
- ✅ Make sure 2-Factor Authentication is enabled
- ✅ Use App Password, NOT your regular Gmail password
- ✅ Remove ALL spaces from app password
- ✅ Generate a new App Password if needed

### "Failed to get a local issuer cert"
- ✅ Already fixed! We're using `CustomEmailBackend` which bypasses SSL verification
- ✅ This is why `EMAIL_BACKEND = 'gtjobfinder.email_backend.CustomEmailBackend'` is set

### "Nodename nor servname provided"
- ✅ This is a network/DNS issue
- ✅ Check your internet connection
- ✅ Try again in a few minutes

---

## Security Notes

⚠️ **Never commit your App Password to Git!**

For production, use environment variables:
```python
import os
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

---

## Switch Back to Mailtrap (Testing)

If you want to switch back to Mailtrap for testing:

```python
EMAIL_BACKEND = 'gtjobfinder.email_backend.CustomEmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@gtjobfinder.com'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'abd587700953a9'
EMAIL_HOST_PASSWORD = '4f80924c5ea6f3'
```

---

## All Set! 🎉

Once you add your Gmail credentials, emails will send for real!
- In-platform messages ✓
- Email notifications ✓
- Password resets ✓
- Any Django email functionality ✓

