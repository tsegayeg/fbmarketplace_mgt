from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('maker', 'Maker'),
        ('checker', 'Checker'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='maker')
    
    # Permission overrides
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="core_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_set",
        related_query_name="user",
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class FacebookAccount(models.Model):
    fb_name = models.CharField(max_length=255)
    fb_email = models.EmailField()
    phone = models.CharField(max_length=20)
    total_posts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.fb_name

    class Meta:
        verbose_name = 'Facebook Account'
        verbose_name_plural = 'Facebook Accounts'

class DailyEntry(models.Model):
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    fb_account = models.ForeignKey(FacebookAccount, on_delete=models.CASCADE)
    posts_today = models.PositiveIntegerField()
    inbox_today = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='Pending')
    checker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='checked_entries')
    checked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Daily Entry'
        verbose_name_plural = 'Daily Entries'