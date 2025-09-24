# Google Maps API Setup

## Quick Setup (2 options)

### Option 1: Get a Google Maps API Key (Recommended)

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select an existing one
3. **Enable the Maps JavaScript API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Maps JavaScript API"
   - Click "Enable"
4. **Create an API Key**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy your API key
5. **Add the key to your Django settings**:
   - Open `gtjobfinder/settings.py`
   - Find the line: `GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"`
   - Replace `YOUR_GOOGLE_MAPS_API_KEY_HERE` with your actual API key
   - Save the file

### Option 2: Use Fallback Version (No API Key Needed)

If you don't want to set up Google Maps API, you can use the fallback version:

1. **Rename the current template**:
   ```bash
   mv jobs/templates/jobs/job_list.html jobs/templates/jobs/job_list_with_maps.html
   ```

2. **Use the fallback template**:
   ```bash
   mv jobs/templates/jobs/job_list_fallback.html jobs/templates/jobs/job_list.html
   ```

The fallback version provides all the same functionality except for the interactive map. It still shows:
- Location-based search
- Distance calculations
- Radius filtering
- One-click applications
- All other features

## Testing

After setting up either option:

1. **Restart your Django server**:
   ```bash
   python manage.py runserver
   ```

2. **Visit the job search page**: http://127.0.0.1:8000/jobs/

3. **Test the features**:
   - Search for jobs
   - Use location services
   - Apply to jobs
   - Check distance filtering

## Troubleshooting

### If maps still don't work:
1. Check that your API key is correct in `settings.py`
2. Make sure the Maps JavaScript API is enabled in Google Cloud Console
3. Check browser console for any error messages
4. Try the fallback version if you don't need the interactive map

### If you get API key errors:
1. Make sure you've enabled the "Maps JavaScript API" in Google Cloud Console
2. Check that your API key has the correct permissions
3. Verify the API key is correctly set in `settings.py`

## Cost Information

- Google Maps API has a free tier with generous limits
- For development and small applications, you likely won't exceed the free tier
- Check Google's pricing page for current rates: https://developers.google.com/maps/billing
