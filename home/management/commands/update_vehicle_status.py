from django.core.management.base import BaseCommand
from django.utils import timezone
from services.models import VehicleRegistration, bookInstantly

class Command(BaseCommand):
    help = 'Automatically update vehicle status based on booking status and drop date/time'

    def handle(self, *args, **options):
        # Get the current date and time
        now = timezone.now()

        # Find vehicle IDs that have bookings with 'Paid' status and overdue drop date/time
        vehicles_to_update_ids = bookInstantly.objects.filter(
            status='Paid',
            dropDate__lte=now.date(),
            dropTime__lte=now.time(),
        ).values_list('vehicle_id', flat=True).distinct()

        # Update the availability status for the found vehicles
        VehicleRegistration.objects.filter(
            id__in=vehicles_to_update_ids,
        ).update(available=True)

        # Update the status of corresponding bookings to 'Done'
        bookInstantly.objects.filter(
            status='Paid',
            dropDate__lte=now.date(),
            dropTime__lte=now.time(),
        ).update(status='Done')

        self.stdout.write(self.style.SUCCESS('Successfully updated vehicle and booking statuses.'))
