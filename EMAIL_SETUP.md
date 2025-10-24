# Email Configuration Guide for GT Job Finder

## 🚀 Quick Setup (Gmail - Recommended)

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled

### Step 2: Generate an App Password

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select app: **Mail**
3. Select device: **Other** (Custom name) → Type "GT Job Finder"
4. Click **Generate**
5. Copy the 16-character password (looks like: `xxxx xxxx xxxx xxxx`)

### Step 3: Update Django Settings

Open `gtjobfinder/settings.py` and update these lines:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # Your App Password (16 chars)
```

### Step 4: Test It!

Run this command to send a test email:

```bash
python3 manage.py shell -c "
from django.core.mail import send_mail
send_mail(
    'Test Email from GT Job Finder',
    'If you receive this, email is working!',
    'noreply@gtjobfinder.com',
    ['your-email@gmail.com'],  # Your email to test
    fail_silently=False,
)
print('✅ Email sent!')
"
```

---

## 🔧 Alternative Email Providers

### Option 2: Outlook/Office 365

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@outlook.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Option 3: SendGrid (Production Ready)

1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key
3. Install package: `pip install sendgrid`

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

### Option 4: AWS SES (Production Ready)

1. Set up [AWS SES](https://aws.amazon.com/ses/)
2. Verify your domain/email
3. Install: `pip install django-ses`

```python
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
```

---

## 🛡️ Security Best Practices

### Using Environment Variables (Recommended)

Instead of hardcoding credentials, use environment variables:

1. Create a `.env` file in your project root:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

2. Add `.env` to `.gitignore`:

```
.env
```

3. Install python-decouple:

```bash
pip install python-decouple
```

4. Update `settings.py`:

```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

---

## 📋 Common Issues & Solutions

### Issue: "SMTPAuthenticationError"
- **Solution**: Make sure you're using an App Password, not your regular Gmail password
- Enable 2-Factor Authentication first

### Issue: "Connection refused"
- **Solution**: Check if your firewall is blocking port 587
- Try port 465 with `EMAIL_USE_SSL = True` instead of `EMAIL_USE_TLS`

### Issue: "Email not received"
- **Solution**: Check spam folder
- Verify the recipient email address is correct
- Check Gmail's "Less secure app access" settings

### Issue: "Daily sending limit exceeded"
- **Solution**: Gmail has a limit of ~500 emails/day for free accounts
- Consider using SendGrid or AWS SES for production

---

## ✅ Testing Checklist

After setup, test these features:

- [ ] Send email from recruiter to job seeker
- [ ] Check email appears in recipient's inbox (not spam)
- [ ] View email log in Email Center
- [ ] Compose new email with candidate search
- [ ] Send email from job applicants page
- [ ] Check email content has proper formatting

---

## 🎯 Current Configuration

Your app is currently configured to use:
- **Provider**: Gmail SMTP
- **Host**: smtp.gmail.com
- **Port**: 587
- **Security**: TLS
- **Status**: ⚠️ Awaiting credentials

**Next step**: Add your Gmail credentials to `settings.py` and restart the server!

