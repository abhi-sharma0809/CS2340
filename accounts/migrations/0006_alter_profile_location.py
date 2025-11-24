# Generated manually to fix NOT NULL constraint

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_latitude_profile_location_profile_longitude'),
    ]

    operations = [
        # First, set default value for existing NULL locations
        migrations.RunSQL(
            sql="UPDATE accounts_profile SET location = 'N/A - Recruiter' WHERE location IS NULL AND user_type = 'recruiter';",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="UPDATE accounts_profile SET location = '' WHERE location IS NULL AND user_type = 'job_seeker';",
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Then alter the field to allow NULL and set default
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, default='', help_text='City, State or City, Country', max_length=200),
        ),
    ]

