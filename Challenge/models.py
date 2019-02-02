from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)
    cover = models.ImageField(upload_to="images")
    distance = models.IntegerField(default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_shops = models.ManyToManyField(Shop, related_name="liked_shops")
    banned_shops = models.ManyToManyField(Shop, related_name="disliked_shops")
