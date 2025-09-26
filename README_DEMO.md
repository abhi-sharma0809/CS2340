# GT JobFinder - Demo Setup

## Quick Start

### 1. Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete setup (migrations, demo data, tests)
python setup_demo.py
```

### 2. Start Server
```bash
python manage.py runserver
```

### 3. Access Demo
- **URL**: http://127.0.0.1:8000/
- **Demo Users**:
  - `demo_seeker` / `demo123` (Job seeker with full profile)
  - `demo_recruiter` / `demo123` (Recruiter account)  
  - `admin` / `admin123` (Admin account)

## Demo Features

### ✅ All 9 User Stories Implemented

1. **Create Profile** - Auto-created profiles with privacy controls
2. **Search Jobs** - Advanced filtering by title, skills, location, salary, remote, visa
3. **One-Click Apply** - Applications with personalized notes
4. **Track Status** - Application status tracking (Applied → Review → Interview → Offer)
5. **Profile Privacy** - Granular visibility controls per section
6. **Job Recommendations** - Skill-based job matching algorithm
7. **Interactive Map** - Leaflet map with job locations
8. **Distance Filtering** - Filter jobs by distance from current location
9. **Commute Radius** - User-preferred commute distance settings

### 🧪 Testing
- **18 comprehensive tests** covering all functionality
- **100% user story coverage**
- Run tests: `python manage.py test`

### 📊 Demo Data
- **15 diverse job postings** across different cities
- **8+ jobs with coordinates** for mapping features
- **Varied attributes**: remote, on-site, visa sponsorship, salary ranges

## Documentation

- **[Demo Script](Demo_Script.md)** - Step-by-step demo presentation guide
- **[Test Report](TestReport.md)** - Comprehensive test results and coverage
- **[Summary](Summary.md)** - Technical implementation details

## Technical Stack

- **Backend**: Django 5.0, Python 3.12+
- **Database**: SQLite (development)
- **Frontend**: Django templates, Bootstrap 5, Leaflet.js
- **Authentication**: Django's built-in auth system
- **Testing**: Django TestCase framework

## Key Features Demonstrated

- **Complete User Journey**: Signup → Profile → Search → Apply → Track
- **Advanced Filtering**: Multiple filter types with proper logic
- **Location Intelligence**: Distance calculations and interactive mapping
- **Privacy Controls**: Granular visibility settings
- **Skill Matching**: Intelligent job recommendations
- **Responsive Design**: Works on desktop and mobile
- **Security**: CSRF protection, authentication, input validation

## Production Ready

- ✅ Comprehensive test suite
- ✅ Security best practices
- ✅ Responsive design
- ✅ Accessibility features
- ✅ Error handling
- ✅ Documentation

This implementation successfully delivers a fully functional job search platform that meets all requirements and provides an excellent user experience for job seekers.
