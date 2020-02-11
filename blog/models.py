from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Blog(models.Model):
     name = models.CharField(max_length=200, help_text="Enter the name of your blog.")
     user = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the post.", blank=False)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    posted_on = models.DateField(auto_now_add=True) # Automatically set the field to now when the object is first created, cannot be edited
    last_modified = models.DateField(default=date.today)

    class Meta: 
        ordering = ['-posted_on']

class Comment(models.Model):
    text = models.TextField(help_text="Body of the comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    posted_on = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)