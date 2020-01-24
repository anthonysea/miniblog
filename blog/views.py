from django.shortcuts import render
from django.views import generic
from blog.models import Blog, Post, Comment
from django.contrib.auth.models import User

class IndexView(generic.TemplateView):
    template_name = 'index.html'
    
    num_blogs = Blog.objects.all().count()
    num_bloggers = User.objects.all().count() - 1
    num_posts = Post.objects.all().count()
    latest_post = Post.objects.latest('posted_on')


    context = {
        'num_blogs': num_blogs,
        'num_bloggers': num_bloggers,
        'num_posts': num_posts,
        'latest_post': latest_post,
    }


class BlogListView(generic.ListView):
    model = Blog


class BloggerListView(generic.ListView):
    model = User


class PostDetailView(generic.DetailView):
    model = Post


class BlogDetailView(generic.DetailView):
    model = Blog