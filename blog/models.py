
from django.db import models
from users.models import User
from django.utils.text import slugify


class Caption(models.Model):
    tag = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.tag
    
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=100, unique=True)
    excerpt = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="images", blank=True)
    caption = models.ManyToManyField(Caption,related_name="caption")
    slug = models.SlugField(max_length=255, default="", blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    
    
class Comment(models.Model):
    name = models.CharField(max_length=20)
    comment = models.TextField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    
    def __str__(self) -> str:
        return self.name