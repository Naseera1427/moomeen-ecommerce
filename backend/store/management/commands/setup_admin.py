import getpass
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Securely creates or updates an administrator account with hashed password."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Administrator username",
        )
        parser.add_argument(
            "--email",
            type=str,
            default="",
            help="Administrator email (optional)",
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Administrator password (if not provided, you will be prompted securely)",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== MOOMEEN PRODUCTS - Secure Admin Setup ==="))

        username = (options.get("username") or "").strip()
        email = (options.get("email") or "").strip()
        password = options.get("password")

        while not username:
            try:
                username = input("Enter admin username: ").strip()
            except (KeyboardInterrupt, EOFError):
                self.stdout.write("\nOperation cancelled.")
                return

            if not username:
                self.stdout.write(self.style.WARNING("Username cannot be empty."))

        if not email and not options.get("username"):
            try:
                email = input("Enter admin email (optional): ").strip()
            except (KeyboardInterrupt, EOFError):
                self.stdout.write("\nOperation cancelled.")
                return

        while not password:
            try:
                password = getpass.getpass("Enter admin password: ")
                if not password:
                    self.stdout.write(self.style.WARNING("Password cannot be empty."))
                    continue
                password_confirm = getpass.getpass("Confirm admin password: ")
                if password != password_confirm:
                    self.stdout.write(self.style.ERROR("Passwords do not match. Please try again."))
                    password = None
                    continue
            except (KeyboardInterrupt, EOFError):
                self.stdout.write("\nOperation cancelled.")
                return

        try:
            validate_password(password)
        except ValidationError as e:
            self.stdout.write(self.style.WARNING(f"Password warning: {', '.join(e.messages)}"))

        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "Created new" if created else "Updated existing"
        self.stdout.write(
            self.style.SUCCESS(
                f"\n[SUCCESS] {action} administrator '{username}' with staff and superuser permissions.\n"
                f"Password has been securely hashed and saved in the database.\n"
                f"You can now log in at /admin-login/ or /admin/.\n"
            )
        )
