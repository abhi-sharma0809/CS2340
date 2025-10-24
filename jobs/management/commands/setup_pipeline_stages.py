from django.core.management.base import BaseCommand
from jobs.models import PipelineStage


class Command(BaseCommand):
    help = 'Set up default pipeline stages for job applications'

    def handle(self, *args, **options):
        default_stages = [
            {
                'name': 'Applied',
                'description': 'Initial application received',
                'order': 1,
                'color': '#6c757d'
            },
            {
                'name': 'Screening',
                'description': 'Initial screening and review',
                'order': 2,
                'color': '#ffc107'
            },
            {
                'name': 'Interview',
                'description': 'Interview scheduled or completed',
                'order': 3,
                'color': '#17a2b8'
            },
            {
                'name': 'Final Review',
                'description': 'Final decision pending',
                'order': 4,
                'color': '#28a745'
            },
            {
                'name': 'Hired',
                'description': 'Candidate accepted the offer',
                'order': 5,
                'color': '#007bff'
            },
            {
                'name': 'Rejected',
                'description': 'Application rejected',
                'order': 6,
                'color': '#dc3545'
            }
        ]

        created_count = 0
        for stage_data in default_stages:
            stage, created = PipelineStage.objects.get_or_create(
                name=stage_data['name'],
                defaults=stage_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created pipeline stage: {stage.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Pipeline stage already exists: {stage.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully set up {created_count} new pipeline stages')
        )
