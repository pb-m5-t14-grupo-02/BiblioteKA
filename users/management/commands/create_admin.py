from django.utils.crypto import get_random_string as grs
from django.core.management.base import BaseCommand
from users.models import User
import dotenv
import os


class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **options):
        dotenv.load_dotenv()
        User.objects.create_superuser(
            username=os.getenv("ADMIN_USERNAME"),
            password=os.getenv("ADMIN_PASSWORD"),
            email=os.getenv("ADMIN_EMAIL") or f"invalid_{grs(4)}@mail.com"
        )
        print("\033[36mAdmin user created ;)")
