from django.db import models
import uuid

class DynamicPage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    api_key = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    slug = models.SlugField(max_length=36, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name