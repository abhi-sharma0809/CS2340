# 📧 Mailtrap Setup (EASIEST Option!)

## Why Mailtrap?

- ✅ **Free forever** (up to 500 emails/month)
- ✅ **No authentication issues** like Gmail/Outlook
- ✅ **Works instantly** - no special setup
- ✅ **See all emails in one place** (like a fake inbox)
- ✅ **Perfect for testing** - emails don't actually send to real people
- ✅ **Beautiful web interface** to view sent emails

## 🚀 Setup (Takes 30 Seconds!)

### Step 1: Sign Up (Free)
1. Go to: **https://mailtrap.io/**
2. Click "Sign Up"
3. Use Google/GitHub or email to sign up (instant, no credit card)

### Step 2: Get Credentials
1. After login, go to **"Email Testing"** section (left sidebar)
2. Click on **"My Inbox"**
3. Select **"SMTP Settings"** dropdown
4. Choose **"Django"**
5. You'll see something like:

```python
EMAIL_HOST_USER = '1a2b3c4d5e6f7g'
EMAIL_HOST_PASSWORD = '9z8y7x6w5v4u3t'
```

### Step 3: Add to Django
1. Open `gtjobfinder/settings.py`
2. Update lines 144-145 with your credentials:

```python
EMAIL_HOST_USER = '1a2b3c4d5e6f7g'  # Copy from Mailtrap
EMAIL_HOST_PASSWORD = '9z8y7x6w5v4u3t'  # Copy from Mailtrap
```

### Step 4: That's It!
- Server auto-reloads
- Send emails through your app
- View them at **mailtrap.io** in your inbox!

## 🎯 How It Works

1. **Your app sends emails** → Mailtrap catches them
2. **View in Mailtrap web interface** → See email content, HTML, attachments
3. **No real emails sent** → Safe for testing with real addresses
4. **Analyze emails** → Check spam score, validate HTML, test links

## 📊 What You Get

- **Email preview** - See exactly what recipients would see
- **HTML & Plain text** versions
- **Spam analysis** - Check if your emails look spammy
- **Email source** - View raw email headers
- **No risk** - Emails never leave Mailtrap

## 🔄 For Production Later

When ready for production, switch to:
- **SendGrid** (free tier: 100 emails/day)
- **AWS SES** (very cheap, scalable)
- **Mailgun** (good for high volume)

Just update the SMTP settings in `settings.py`!

---

## 💡 Quick Test

After adding credentials, test it:

```bash
python3 manage.py shell -c "
from django.core.mail import send_mail
send_mail(
    'Test from GT Job Finder',
    'It works!',
    'noreply@gtjobfinder.com',
    ['test@example.com'],
)
print('✅ Check your Mailtrap inbox!')
"
```

Then check **mailtrap.io** → **My Inbox** to see the email!

