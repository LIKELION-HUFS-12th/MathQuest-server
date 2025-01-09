from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    name = models.CharField(max_length=100)
    birthdate = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)

    # Add related_name attributes to prevent conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username
