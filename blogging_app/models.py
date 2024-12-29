from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
    
    def __str__(self):
        return self.title