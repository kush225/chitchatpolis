# myapp/management/commands/populate_users.py

from django.core.management.base import BaseCommand
from api.models import User
import random
import string

class Command(BaseCommand):
    help = 'Populate users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        for i in range(1,count):
            name = f'test{i}'
            email = f'{name}@example.com'
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            User.objects.create_user(name=name, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} users'))
