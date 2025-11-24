# Admin Panel Guide

## Overview
The GT Job Finder Admin Panel provides comprehensive tools for platform administrators to manage users, moderate content, and export data for analysis.

## Access Requirements
- **User must be staff**: `user.is_staff = True`
- **Or superuser**: `user.is_superuser = True`

## Creating an Admin User

### Option 1: Using Django Shell
```bash
python3 manage.py shell
```

```python
from django.contrib.auth.models import User

# Create a new admin user
admin = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='your_secure_password',
    is_staff=True,
    is_superuser=True
)
```

### Option 2: Using Django Management Command
```bash
python3 manage.py createsuperuser
```

### Option 3: Promote Existing User to Admin
```bash
python3 manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.get(username='your_username')
user.is_staff = True
user.is_superuser = True
user.save()
```

## Features

### 1. User Management (User Story: Manage Users and Roles)
**Location**: Admin Dashboard → User Management

**Capabilities**:
- ✅ **View All Users**: See complete list with filtering options
- ✅ **Search Users**: Search by username, email, first name, or last name
- ✅ **Filter by Type**: Filter by Job Seeker or Recruiter
- ✅ **Change Roles**: Switch users between job_seeker and recruiter roles
- ✅ **Activate/Deactivate**: Enable or disable user accounts
- ✅ **Delete Users**: Permanently remove users from the platform
- ✅ **Protected Accounts**: Superusers cannot be modified or deleted

**Safety Features**:
- Confirmation dialogs for all destructive actions
- Superuser accounts are protected from modification
- Real-time status updates

**Example Use Cases**:
1. **Spam Account**: Deactivate account → Monitor → Delete if necessary
2. **Role Request**: User asks to become recruiter → Change role via Switch Role button
3. **Account Abuse**: Immediately deactivate → Review → Delete

---

### 2. Job Moderation (User Story: Moderate Job Posts)
**Location**: Admin Dashboard → Job Moderation

**Capabilities**:
- ✅ **View All Jobs**: See all job postings with details
- ✅ **Search Jobs**: Search by title, company, location, or description
- ✅ **Filter by Status**: Show only active or inactive jobs
- ✅ **Activate/Deactivate**: Control job visibility
- ✅ **Delete Jobs**: Remove spam or abusive job posts
- ✅ **View Details**: See job skills, posting date, and recruiter info

**Safety Features**:
- Confirmation dialogs before deletion
- Visual status indicators (Active/Inactive)
- Ability to deactivate first, then delete if needed

**Example Use Cases**:
1. **Spam Job Post**: Deactivate immediately → Review → Delete if spam
2. **Inappropriate Content**: Delete job post and message/warn recruiter
3. **Expired Jobs**: Bulk deactivate old positions
4. **Quality Control**: Review new posts for appropriateness

---

### 3. Data Export (User Story: Export Data for Reporting)
**Location**: Admin Dashboard → Export Platform Data

**Available Exports**:

#### **Export Users CSV**
Includes:
- User ID, Username, Email
- First Name, Last Name
- User Type (Job Seeker/Recruiter)
- Account Status (Active/Inactive)
- Staff Status
- Join Date
- Location, Skills
- Profile Visibility

**Use Cases**:
- Monthly user growth reports
- User demographic analysis
- Stakeholder presentations
- Platform statistics

---

#### **Export Jobs CSV**
Includes:
- Job ID, Title, Company
- Location, Job Type
- Experience Level
- Salary Range (Min/Max)
- Active Status
- Posted By (username)
- Creation Date
- Application Count

**Use Cases**:
- Job market analysis
- Recruiter activity reports
- Popular job types/locations
- Application conversion rates

---

#### **Export Applications CSV**
Includes:
- Application ID
- Job Title, Company
- Applicant Username, Email
- Application Status
- Application Date
- Cover Letter Preview (first 100 chars)

**Use Cases**:
- Hiring funnel analysis
- Time-to-hire metrics
- Application status distribution
- Candidate engagement tracking

---

## Admin Dashboard Statistics

**Real-time Metrics**:
- 📊 **Total Users** (with Job Seeker/Recruiter breakdown)
- 💼 **Total Jobs** (with Active job count)
- 📝 **Total Applications**
- 💬 **Total Messages**

**Recent Activity**:
- Last 5 registered users
- Last 5 posted jobs
- Quick access to details

---

## Navigation

The Admin link appears in the navigation bar for all staff/superuser accounts:

```
🛡️ Admin (highlighted in red)
```

**Admin Pages**:
1. **Dashboard** - Statistics and recent activity
2. **User Management** - Manage all user accounts
3. **Job Moderation** - Moderate job postings

---

## Security Notes

### Protected Actions
- Superusers cannot be deactivated, deleted, or have roles changed
- All destructive actions require confirmation
- Staff status required for access (`@staff_member_required`)

### Best Practices
1. **Always deactivate before deleting**: Gives you time to review
2. **Export data regularly**: Maintain backup records
3. **Document admin actions**: Keep notes on why accounts were removed
4. **Review recent activity**: Check dashboard regularly for suspicious activity

---

## Troubleshooting

### "Access Denied"
- Ensure `user.is_staff = True` or `user.is_superuser = True`
- Log out and log back in after promoting to admin

### CSV Downloads Not Working
- Check browser popup blocker
- Ensure proper file permissions
- Try different browser if issues persist

### Actions Not Working
- Ensure JavaScript is enabled
- Check browser console for errors
- Verify CSRF token is present

---

## URL Structure

```
/accounts/admin/                            # Dashboard
/accounts/admin/users/                      # User Management
/accounts/admin/jobs/                       # Job Moderation
/accounts/admin/export/?type=users          # Export Users
/accounts/admin/export/?type=jobs           # Export Jobs
/accounts/admin/export/?type=applications   # Export Applications
```

---

## API Endpoints (Internal)

### User Management
- `POST /accounts/admin/users/<id>/toggle-status/` - Activate/Deactivate
- `POST /accounts/admin/users/<id>/change-role/` - Change user type
- `POST /accounts/admin/users/<id>/delete/` - Delete user

### Job Moderation
- `POST /accounts/admin/jobs/<id>/toggle-status/` - Activate/Deactivate
- `POST /accounts/admin/jobs/<id>/delete/` - Delete job

---

## Example Workflows

### Weekly Moderation Routine
1. Check dashboard for activity overview
2. Review new users (last 5-10 users)
3. Check recent job posts for spam
4. Export weekly data for stakeholders
5. Address any flagged content

### Monthly Reporting
1. Export users CSV → Analyze growth trends
2. Export jobs CSV → Popular positions/locations
3. Export applications CSV → Conversion metrics
4. Create summary report with insights
5. Share with stakeholders

### Handling Reports
1. **Spam User Report**:
   - Search for user in User Management
   - Review their activity (jobs posted, applications)
   - Deactivate account
   - Monitor for 24-48 hours
   - Delete if confirmed spam

2. **Inappropriate Job Post**:
   - Search job in Job Moderation
   - Deactivate immediately
   - Send message to recruiter (via dashboard)
   - Delete if violates terms
   - Document action

---

## Future Enhancements

Potential additions for future versions:
- [ ] User activity logs (login history, actions)
- [ ] Automated spam detection
- [ ] Bulk actions (select multiple → activate/deactivate/delete)
- [ ] Admin action audit log
- [ ] Email notifications for admin actions
- [ ] Dashboard graphs and charts
- [ ] Advanced search filters
- [ ] User reports/flagging system
- [ ] Custom data date ranges for exports

---

## Support

For technical issues or feature requests related to the admin panel:
1. Check Django logs for errors
2. Verify database integrity
3. Test with different admin accounts
4. Review browser console for JavaScript errors

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Satisfies User Stories**: Administrator User Management, Job Moderation, Data Export

