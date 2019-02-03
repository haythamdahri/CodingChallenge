from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)
    cover = models.ImageField(upload_to="images")
    distance = models.IntegerField(default=0)

    def __repr__(self):
        return f"NAME: {self.name}"
    def __str__(self):
        return f"NAME: {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_shops = models.ManyToManyField(Shop, related_name="liked_shops", blank=True)
    banned_shops = models.ManyToManyField(Shop, related_name="disliked_shops", blank=True)

    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"PROFILE: {self.fullname()} | SHOPS: {self.preferred_shops.all().count()}"
