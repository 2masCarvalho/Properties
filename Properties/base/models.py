from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    USER_TYPES = (
        ('host', 'Host'),
        ('guest', 'Guest'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='guest')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.png')

    def __str__(self):
        return f'{self.user.username} Profile'


class Property(models.Model):
    LOCATION_CHOICES = [
        ('faro', 'Faro'),
        ('lagos', 'Lagos'),
        ('portimao', 'Portimão'),
        ('albufeira', 'Albufeira'),
        ('tavira', 'Tavira'),
        ('olhao', 'Olhão'),
        ('silves', 'Silves'),
        ('loule', 'Loulé'),
        ('vila_real_de_santo_antonio', 'Vila Real de Santo António'),
    ]
    host = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    area = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    elevator = models.BooleanField(default=False)
    parking_spaces = models.IntegerField(default=0)
    pool = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey('Property', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
