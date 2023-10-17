from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            "user_id": self.id,
            "user_email":self.email,
            "user_username":self.username,
        }

class Follow(models.Model):
    user_followed = models.ForeignKey("User",on_delete=models.CASCADE,related_name="user_followed")
    followers = models.ManyToManyField("User",blank=True,related_name="followers")

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="poster")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField()
    likes = models.ManyToManyField("User", blank=True, related_name="likes")
    edited = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "poster_username": self.poster.username,
            "poster_email":self.poster.email,
            "poster_id":self.poster.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }