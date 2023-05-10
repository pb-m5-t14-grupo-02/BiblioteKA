from django.utils.crypto import get_random_string as grs
from django.core.management.base import BaseCommand
from users.models import User
from names import get_first_name
from random import choice

class Command(BaseCommand):
    help = "Create users"

    def add_arguments(self, parser):
        parser.add_argument(
            "total",
            type=int,
            help="Indicates the number of users to be created"
        )
    def handle(self, *args, **options):
        total = options.get("total")
        option = [True, False]
        for i in range(total):
            User.objects.create_user(
                username=get_first_name().lower(),
                email=grs(5) + "@mail.com",
                password="1234",
                is_student=choice(option),
                is_colaborator=choice(option)
            )
        print("\033[35mUsers created ,D")

