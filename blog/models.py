from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Blog(models.Model):
     name = models.CharField(max_length=200, help_text="Enter the name of your blog.")
     user = models.ForeignKey(User, on_delete=models.SET_NULL)

class Post(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the post.", required=True)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, on_delete=models.SET_NULL)
    body = models.TextField()
    posted_on = models.DateField(auto_now_add=True) # Automatically set the field to now when the object is first created, cannot be edited
    last_edited_on = models.DateField(default=date.today())

class Comment(models.Model):
    text = models.TextField(help_text="Body of the comment")