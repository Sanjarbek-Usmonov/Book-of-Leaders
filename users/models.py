from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField('Phone Number',
                                max_length=13, unique=True)
    full_name = models.CharField(max_length=70)
    # email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name',
                        'gender', 'password']

    def __str__(self):
        return "{} {}".format(self.username, self.full_name)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
