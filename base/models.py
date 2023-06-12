from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import secrets

# user registration model
class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# access key model
class AccessKey(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')
    procurement_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    access_key = models.CharField(max_length=32, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if self.status == 'active':
            AccessKey.objects.filter(user=self.user, status='active').update(status='inactive')
        if not self.access_key:
            self.access_key = secrets.token_hex(16)
        self.expiry_date = self.procurement_date + timezone.timedelta(days=3)
        super().save(*args, **kwargs)
