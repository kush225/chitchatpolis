from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, email, name, password=None, **extra_fields):
        """
        Method to create a new user.
        """
        # Check if email is provided
        if not email:
            raise ValueError('The Email field must be set')

        # Normalize email address
        email = self.normalize_email(email)

        # Create and save the user with provided details
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class LowercaseCharField(models.EmailField):
    """
    Custom EmailField that converts email value to lowercase before saving.
    """

    def get_prep_value(self, value):
        """
        Convert the email value to lowercase.
        """
        return str(value).lower()

class User(AbstractBaseUser):
    """
    Custom User model extending AbstractBaseUser.
    """

    email = LowercaseCharField(unique=True, blank=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        Return string representation of the user (email).
        """
        return self.email
