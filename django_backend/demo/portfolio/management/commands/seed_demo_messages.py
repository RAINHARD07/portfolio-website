from django.core.management.base import BaseCommand
from django.utils import timezone

from portfolio.models import ContactSubmission


class Command(BaseCommand):
    help = "Create clearly marked demo contact submissions for inbox load testing."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=200001)
        parser.add_argument("--batch-size", type=int, default=1000)

    def handle(self, *args, **options):
        count = options["count"]
        batch_size = options["batch_size"]
        if count < 1 or batch_size < 1:
            self.stderr.write("count and batch-size must be positive integers")
            return

        now = timezone.now()
        for start in range(0, count, batch_size):
            end = min(start + batch_size, count)
            ContactSubmission.objects.bulk_create([
                ContactSubmission(
                    name=f"Demo Visitor {index + 1}",
                    email=f"demo-{index + 1}@example.invalid",
                    subject="[DEMO] Inbox load test",
                    message_body=f"This is demo message {index + 1} for inbox load testing.",
                    submitted_at=now,
                    is_reviewed=True,
                )
                for index in range(start, end)
            ], batch_size=batch_size)
            self.stdout.write(f"Created {end:,}/{count:,} demo messages")

        self.stdout.write(self.style.SUCCESS(f"Created {count:,} demo messages."))