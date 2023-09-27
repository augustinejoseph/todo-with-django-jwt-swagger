from django.db import models
from django.contrib.auth.models import User


class TodoTask(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
