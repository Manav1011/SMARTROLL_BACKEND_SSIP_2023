from Manage.utils import send_notification_async
import threading
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Cronjob'

    def handle(self, *args, **options):        
        thread = threading.Thread(target=send_notification_async,kwargs={"time":"14:00:00"})
        thread.start()
        self.stdout.write('My custom command executed successfully')