from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


# Custom User Manager for handling user creation
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)  # Normalize email
        user = self.model(email=email, username=username, **extra_fields)

        if password:
            user.set_password(password)  # Set a hashed password

        user.save(using=self._db)  # Save the user instance to the database
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Unique email identifier
    username = models.CharField(max_length=30, unique=True)  # Unique username
    first_name = models.CharField(max_length=30, blank=True)  # Optional first name
    last_name = models.CharField(max_length=30, blank=True)  # Optional last name
    is_active = models.BooleanField(default=True)  # Is the user active?
    is_staff = models.BooleanField(default=False)  # Is the user staff?
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"  # Use email for authentication
    REQUIRED_FIELDS = ["username"]  # Additional required fields for superusers

    def __str__(self):
        return self.username
