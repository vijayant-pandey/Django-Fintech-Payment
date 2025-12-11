# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     # Add related_name to avoid clashes
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='custom_user_set',  # Custom related_name
#         blank=True,
#         help_text=(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         verbose_name='groups',
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='custom_user_set',  # Custom related_name
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
