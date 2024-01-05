from django.core.management.base import BaseCommand, CommandParser 
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create Application User'
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--email', type=str, help="User's email")
        parser.add_argument('--username', type=str, help="User's name")
        parser.add_argument('--password', type=str, help="User's password")
        parser.add_argument('--is_admin', type=bool, default=False, help="User is admin")
        
    def handle(self, *args, **options) -> None:
        email: str = options['email']
        username: str = options['username']
        password: str = options['password']
        is_admin: bool = options['is_admin']
        
        User = get_user_model()
        if email and username and password:
            if not User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists():
                User.objects.create_user(email=email, password=password, username=username, is_admin=is_admin)
                self.stdout.write(self.style.SUCCESS('Admin user created successfully.'))
            else:
                self.stdout.write(self.style.WARNING('Admin user already exists.'))
        else:
            self.stdout.write(self.style.ERROR('Please provide --email, --name, and --password arguments.'))