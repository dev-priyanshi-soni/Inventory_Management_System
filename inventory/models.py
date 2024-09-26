
from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
