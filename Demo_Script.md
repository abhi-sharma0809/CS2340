# GT JobFinder - Demo Script

## Pre-Demo Setup

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd gtjobfinder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load demo data
python manage.py loaddata fixtures/demo.json

# Set up demo user passwords
python setup_demo_users.py

# Start development server
python manage.py runserver
```

### 2. Demo Users
- **demo_seeker** / demo123 (Job seeker with full profile)
- **demo_recruiter** / demo123 (Recruiter account)
- **admin** / admin123 (Admin account)

## Demo Flow (15-20 minutes)

### Introduction (2 minutes)
"Welcome to GT JobFinder, a comprehensive job search platform built with Django. Today I'll demonstrate all 9 core user stories for job seekers, showing how our platform helps users find, apply to, and track job opportunities."

### 1. User Registration & Profile Creation (2 minutes)
**Story**: Create Profile
- Navigate to home page: `http://127.0.0.1:8000/`
- Click "Get Started" → Sign up
- Create new user: `newuser` / `password123`
- **Show**: Profile automatically created
- Navigate to "My Profile"
- **Demonstrate**: Edit profile form
- Add headline: "Full-Stack Developer with Python expertise"
- Add skills: "Python, Django, JavaScript, React, SQL"
- Add education: "Georgia Tech - Computer Science"
- Add experience: "Software Engineer Intern at TechCorp"
- Add links: "https://github.com/newuser"
- **Show**: Privacy controls (skills, education, experience, links)
- **Show**: Commute radius setting (25 km)

### 2. Job Search & Filtering (3 minutes)
**Story**: Search Jobs with Filters
- Navigate to "Jobs" in navbar
- **Show**: Job list with 15+ demo jobs
- **Demonstrate filters**:
  - Search by title: "Python"
  - Filter by remote work: Check "Remote"
  - Filter by visa sponsorship: Check "Visa Sponsorship"
  - Filter by salary: Min $80,000, Max $150,000
  - Filter by location: "Atlanta"
- **Show**: Results update dynamically
- **Show**: Job cards with company logos, salary ranges, badges

### 3. Job Application with Notes (2 minutes)
**Story**: One-Click Apply + Tailored Note
- Click on "Senior Python Developer" job
- **Show**: Job detail page with company info, description, location map
- Click "Apply Now" button
- **Show**: Modal form with note field
- Add note: "I'm very excited about this opportunity! My Python and Django experience aligns perfectly with your requirements."
- Submit application
- **Show**: Success message and "Already Applied" status
- **Demonstrate**: Can't apply twice (idempotent)

### 4. Application Tracking (1 minute)
**Story**: Track Status
- Navigate to "My Applications"
- **Show**: Application list with status "Applied"
- **Show**: Application details including note
- **Note**: Status can be updated by recruiters via admin panel

### 5. Profile Privacy (1 minute)
**Story**: Profile Privacy Options
- Navigate to "My Profile"
- **Show**: Privacy controls sidebar
- Toggle "Show Skills" to hidden
- Navigate to public profile: `/accounts/u/newuser/`
- **Show**: Skills section hidden from public view
- **Show**: Headline always visible (always public)

### 6. Job Recommendations (2 minutes)
**Story**: Job Recommendations Based on Skills
- Navigate to "Recommended" in navbar
- **Show**: Jobs ranked by skill matches
- **Explain**: Algorithm matches user skills with job titles/descriptions
- **Show**: "Python Developer" and "Full Stack Developer" ranked highly
- **Show**: Scoring based on skill frequency in job descriptions

### 7. Interactive Job Map (3 minutes)
**Story**: Interactive Map of Job Postings
- Navigate to "Map" in navbar
- **Show**: Leaflet map with job markers
- **Demonstrate**: Click markers to see job details
- **Show**: Popup with job title, company, link to detail page

### 8. Distance Filtering (2 minutes)
**Story**: Filter Jobs on Map by Distance
- Click "Use Current Location" button
- **Show**: Browser geolocation prompt
- **Show**: Map centers on current location
- **Show**: Distance badges on job markers
- **Demonstrate**: Radius filter (10, 25, 50, 100 km)
- **Show**: Jobs filter by distance in real-time
- **Show**: Job list updates with distance information

### 9. Preferred Commute Radius (1 minute)
**Story**: Preferred Commute Radius
- **Show**: User's commute radius (25 km) pre-selected in radius filter
- **Explain**: This preference is saved in user profile
- **Show**: Map uses this as default when user is logged in

### Advanced Features Demo (2 minutes)

#### Multiple User Perspectives
- Logout and login as `demo_seeker` / `demo123`
- **Show**: Pre-populated profile with skills
- **Show**: Recommended jobs based on existing skills
- **Show**: Different commute radius preference

#### Admin Panel
- Login as `admin` / `admin123`
- Navigate to `/admin/`
- **Show**: Job management
- **Show**: Application status updates
- **Show**: User management

### Technical Highlights (1 minute)
- **Show**: Responsive design (resize browser)
- **Show**: Clean, professional UI with GT branding
- **Show**: Fast page loads and smooth interactions
- **Show**: Proper error handling and user feedback

## Demo Conclusion (1 minute)
"GT JobFinder successfully implements all 9 user stories for job seekers:
1. ✅ Profile creation with privacy controls
2. ✅ Advanced job search with multiple filters
3. ✅ One-click applications with personalized notes
4. ✅ Application status tracking
5. ✅ Granular privacy controls
6. ✅ Skill-based job recommendations
7. ✅ Interactive job location mapping
8. ✅ Distance-based filtering
9. ✅ Personalized commute preferences

The platform is production-ready with comprehensive testing, security features, and a modern, accessible user interface."

## Troubleshooting

### Common Issues
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **Database errors**: Run `python manage.py migrate` again
- **Missing demo data**: Re-run `python manage.py loaddata fixtures/demo.json`
- **Geolocation not working**: Use manual location input in map view

### Demo Tips
- **Prepare**: Test the demo flow beforehand
- **Backup**: Have screenshots ready in case of technical issues
- **Timing**: Keep each section under 3 minutes
- **Engagement**: Ask questions and encourage interaction
- **Flexibility**: Skip sections if running short on time

## Post-Demo
- **Q&A**: Answer questions about implementation
- **Code Review**: Show key code snippets if requested
- **Deployment**: Discuss production deployment options
- **Future Enhancements**: Discuss potential improvements
