# Testing Guide - All User Stories

## Sample Data Overview

The database has been populated with comprehensive sample data to test all user stories.

### Test Accounts (All passwords: `password123`)

#### Job Seekers (8 accounts)
| Username | Name | Role | Location | Key Skills |
|----------|------|------|----------|------------|
| demo_alice | Alice Johnson | Full Stack Developer | Atlanta, GA | Python, Django, React, JavaScript |
| demo_bob | Bob Smith | Data Scientist | San Francisco, CA | Python, ML, TensorFlow, PyTorch |
| demo_carol | Carol Williams | Frontend Developer | New York, NY | React, Vue.js, TypeScript, CSS |
| demo_david | David Martinez | DevOps Engineer | Austin, TX | AWS, Docker, Kubernetes, Terraform |
| demo_emma | Emma Davis | Product Manager | Seattle, WA | Agile, Analytics, SQL |
| demo_frank | Frank Garcia | Backend Engineer | Boston, MA | Java, Spring Boot, Microservices |
| demo_grace | Grace Lee | Mobile Developer | Los Angeles, CA | Swift, Kotlin, React Native |
| demo_henry | Henry Chen | Security Engineer | Washington, DC | Cybersecurity, Penetration Testing |

#### Recruiters (3 accounts)
| Username | Company | Location |
|----------|---------|----------|
| demo_recruiter_google | Google | Mountain View, CA |
| demo_recruiter_amazon | Amazon | Seattle, WA |
| demo_recruiter_startup | TechFlow Solutions | Atlanta, GA |

### Sample Data Created
- **Job Seekers**: 8 with complete profiles
- **Education Entries**: 9 (LinkedIn-style structured data)
- **Work Experience Entries**: 10 (LinkedIn-style structured data)
- **Job Postings**: 10 across different companies and locations
- **Applications**: 15 with various statuses
- **Messages**: 4 conversations between recruiters and candidates

---

## Testing User Stories

### Job Seeker User Stories

#### 1. Create Profile with Skills, Education, Experience ✓

**Test Steps:**
1. Login as: `demo_alice` / `password123`
2. Navigate to Profile → View Profile
3. **Verify**:
   - Headline: "Full Stack Developer | React & Python Expert"
   - Skills are visible
   - Education entries show:
     - Georgia Tech - BS Computer Science (GPA 3.85)
     - Georgia Tech - MS Computer Science (GPA 3.92)
   - Work experience shows:
     - Google internship
     - Current position at Tech Startup Inc

#### 2. Search for Jobs with Filters ✓

**Test Steps:**
1. Login as: `demo_alice`
2. Go to Jobs → Search Jobs
3. **Test Filters:**
   - Search by title: "Engineer"
   - Filter by location: "Atlanta, GA" with radius
   - Filter by salary range
   - Toggle "Remote Only"
   - Toggle "Visa Sponsorship"
4. **Verify**: Results update based on filters

#### 3. Apply to Job with One Click ✓

**Test Steps:**
1. Login as: `demo_alice`
2. Find any job (e.g., "Senior Full Stack Engineer")
3. Click "Apply Now"
4. Add optional note: "I'm very interested in this position"
5. Submit application
6. **Verify**:
   - Success message appears
   - Application saved to My Applications
   - Cannot apply twice (duplicate prevention)

#### 4. Track Application Status ✓

**Test Steps:**
1. Login as: `demo_alice`
2. Go to My Applications
3. **Verify**:
   - See all applications
   - Status cards show counts: Applied, Under Review, Interview, Accepted, Rejected
   - **Click status cards** to filter applications (NEW FEATURE!)
   - View status history timeline

#### 5. Set Privacy Options ✓

**Test Steps:**
1. Login as: `demo_alice`
2. Go to Profile → Edit Profile
3. Toggle privacy settings:
   - Global profile visibility
   - Show/hide skills
   - Show/hide education
   - Show/hide experience
   - Show/hide links
4. Save changes
5. **Verify**: Changes reflected on public profile

#### 6. Receive Job Recommendations ✓

**Test Steps:**
1. Login as: `demo_alice` (has Python, React skills)
2. Go to Jobs → Recommended Jobs
3. **Verify**:
   - See jobs matching skills
   - Jobs are **clickable** (NEW FEATURE!)
   - Relevant positions shown (Full Stack, Backend, etc.)

#### 7. View Jobs on Interactive Map ✓

**Test Steps:**
1. Login as: `demo_alice`
2. Go to Jobs → Search Jobs
3. Scroll to map section
4. **Verify**:
   - Your location marker appears
   - Job markers show on map
   - Click markers for job details
   - Distance shown from your location

#### 8. Filter Jobs by Distance ✓

**Test Steps:**
1. Login as: `demo_alice` (location: Atlanta)
2. On jobs page, use distance filter
3. Set radius (10 km, 25 km, 50 km, etc.)
4. **Verify**: Only jobs within radius shown

#### 9. Set Commute Radius Preference ✓

**Test Steps:**
1. Login as: `demo_alice`
2. Edit Profile
3. Set "Preferred Commute Radius" (default 10 km)
4. Save
5. **Verify**: Map filters respect this preference

---

### Recruiter User Stories

#### 1. Post and Edit Job Roles ✓

**Test Steps:**
1. Login as: `demo_recruiter_google` / `password123`
2. Dashboard → "Post New Job"
3. Fill out form:
   - **Use interactive map** to pin location (NEW FEATURE!)
   - Click map or drag marker
   - Coordinates auto-fill
4. Submit job posting
5. Edit job from My Jobs
6. **Verify**: Job saved and editable

#### 2. Search Candidates by Skills/Location ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. Dashboard → **Large "Find the Perfect Candidates" banner** (NEW!)
3. Click "Search Candidates Now"
4. Search by:
   - Skills: "Python" OR "React" (**NEW OR logic**)
   - Location: "San Francisco" with radius
   - Education: "Stanford"
   - Experience: "Engineer"
5. **Verify**:
   - Results show candidates matching **ANY** criteria (not all)
   - **No percent match** displayed (NEW!)
   - Match reasons clearly explain why candidate surfaced

#### 3. Organize Applicants in Pipeline (Kanban) ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. Go to My Jobs → Select "Senior Full Stack Engineer"
3. Click "Applicants"
4. Click "Pipeline Management"
5. **Verify**:
   - Kanban board with stages
   - Drag applicants between stages
   - Status updates automatically

#### 4. Message Candidates In-Platform ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. View applicants for any job
3. Click "Message" on a candidate
4. Send message
5. Switch to `demo_alice` account
6. Go to Messages
7. **Verify**: Message received and can reply

#### 5. Email Candidates Through Platform ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. View applicants
3. Click "Email" button
4. Send email
5. **Verify**: Email logged in system

#### 6. Save Candidate Search & Get Notifications ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. Perform candidate search
3. Click "Save Search"
4. Name it and enable notifications
5. Go to Saved Searches
6. **Verify**: Search saved, can re-run it

#### 7. Receive Candidate Recommendations (NEW!) ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. Go to "Senior Full Stack Engineer" job
3. Click "Applicants"
4. **Click "Recommended Candidates" tab** (NEW!)
5. **Verify**:
   - Top 25 candidates shown
   - Match scores and reasons displayed
   - Can message candidates directly
   - View full profiles

#### 8. Pin Job Location on Map (NEW!) ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. Post New Job OR Edit existing job
3. In Location section:
   - **See interactive map** (NEW!)
   - Click anywhere to pin location
   - Drag marker to adjust
   - Use "Search Address" button
   - Use "My Current Location"
4. **Verify**: Coordinates auto-fill, location saved

#### 9. See Applicant Clusters on Map (NEW!) ✓

**Test Steps:**
1. Login as: `demo_recruiter_google`
2. Go to any job with applicants
3. Click "Applicants Map" button (NEW!)
4. **Verify**:
   - Job location shown as red marker
   - Applicants shown as blue markers
   - **Clusters form** for nearby candidates
   - Click cluster to expand
   - Click marker for candidate details
   - Statistics panel shows:
     - Avg distance from job
     - Applicants within 50km
     - Top 5 cities

---

### Administrator User Stories

#### 1. Manage Users and Roles ✓

**Test Steps:**
1. Create admin account: `python manage.py createsuperuser`
2. Login to Django admin: `/admin/`
3. OR use accounts admin: `/accounts/admin/`
4. **Verify**:
   - View all users
   - Search users
   - Filter by user type
   - Change roles
   - Activate/deactivate accounts
   - Delete users (with confirmation)

#### 2. Moderate/Remove Job Posts ✓

**Test Steps:**
1. Login as admin
2. Go to `/accounts/admin/jobs/`
3. **Verify**:
   - View all job postings
   - Search by title, company, location
   - Filter by active/inactive status
   - Activate/deactivate jobs
   - Delete inappropriate jobs

#### 3. Export Data for Reporting ✓

**Test Steps:**
1. Login as admin
2. Go to `/accounts/admin/export/`
3. Export options:
   - Users to CSV
   - Jobs to CSV
   - Applications to CSV
4. **Verify**: CSV files download with complete data

---

## New Features to Test

### 1. Clickable Status Cards ✓

**Location**: My Applications page (job seeker view)

**Test:**
1. Login as: `demo_alice`
2. Go to My Applications
3. **Click different status cards:**
   - Total Applications → Shows all
   - Applied → Shows only "Applied" status
   - Under Review → Shows only "Reviewed" status
   - Interview → Shows only "Interview" status
   - Accepted → Shows only accepted
   - Rejected → Shows only rejected
4. **Verify**:
   - Active filter highlighted with blue gradient
   - Applications filter instantly
   - Smooth scroll to results

### 2. OR Search Logic (Include Any) ✓

**Location**: Candidate Search (recruiter view)

**Test:**
1. Login as: `demo_recruiter_google`
2. Search candidates with:
   - Skills: "Python, Machine Learning"
   - Location: "California"
3. **Before**: Required ALL (Python AND ML AND California)
4. **Now**: Shows candidates with Python OR ML OR California
5. **Verify**: More inclusive results

### 3. No Percent Match Display ✓

**Location**: Candidate Search results

**Test:**
1. Login as: `demo_recruiter_google`
2. Search for candidates
3. **Verify**:
   - NO "X% match" badges
   - Clean card design
   - Match reasons still shown (e.g., "Matching skills: Python, React")

### 4. Prominent Candidate Search ✓

**Location**: Recruiter Dashboard

**Test:**
1. Login as: `demo_recruiter_google`
2. View dashboard
3. **Verify**:
   - Large navy blue banner at top
   - "Find the Perfect Candidates" heading
   - Gold "Search Candidates Now" button
   - "Saved Searches" button
   - Eye-catching design

### 5. Structured Education & Experience ✓

**Location**: Profile pages

**Test:**
1. Login as: `demo_alice`
2. View Profile
3. **Verify Education** shows:
   - School name
   - Degree and field
   - GPA (if provided)
   - Start/end dates
   - Description
4. **Verify Work Experience** shows:
   - Job title
   - Company
   - Location
   - Dates
   - "Current" indicator
   - Description

---

## Quick Testing Scenarios

### Scenario 1: Job Seeker Journey
1. Login as `demo_alice`
2. View recommended jobs (based on Python, React skills)
3. Apply to "Senior Full Stack Engineer" at Google
4. Track application status
5. Receive message from Google recruiter
6. Reply to message

### Scenario 2: Recruiter Journey
1. Login as `demo_recruiter_google`
2. Post new job with map location pin
3. View "My Jobs Map" to see all job locations
4. Search candidates with OR logic
5. View candidate recommendations for job
6. View applicant cluster map
7. Message a candidate
8. Move candidate through pipeline

### Scenario 3: Testing New Features
1. Login as `demo_alice`
2. Test clickable status cards on My Applications
3. Switch to `demo_recruiter_google`
4. Test prominent search banner
5. Test OR search logic
6. Verify no percent match shown
7. Test applicant map clustering
8. Test job location pinning

---

## Data Cleanup

To reset and reseed data:
```bash
python manage.py seed_sample_data
```

This will:
- Delete all demo_ accounts
- Create fresh sample data
- Reset all test scenarios

---

## Notes

- All passwords: `password123`
- Sample data uses realistic company names (Google, Amazon, etc.)
- Geographic locations are accurate with real coordinates
- Applications have varied statuses for testing filters
- Messages demonstrate recruiter-candidate communication
- Education and work experience demonstrate LinkedIn-style profiles

---

## Contact for Issues

If you encounter any issues during testing:
1. Check that migrations are applied: `python manage.py migrate`
2. Verify sample data loaded: Check counts in admin panel
3. Clear browser cache if UI doesn't update
4. Check console for JavaScript errors (F12)

---

**Happy Testing!** 🎉
