from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from blog.models import Blog, Post, Comment
from django.contrib.auth.models import User

class IndexView(generic.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        """Override get_context_data() to be able to add additional items in the context dict to be available on the template"""
        context = super().get_context_data(**kwargs) # Need to call and set using parent method first

        num_blogs = Blog.objects.all().count()
        num_bloggers = User.objects.all().count() - 1
        num_posts = Post.objects.all().count()
        latest_post = Post.objects.latest('posted_on')

        context.update({
            'num_blogs': num_blogs,
            'num_bloggers': num_bloggers,
            'num_posts': num_posts,
            'latest_post': latest_post,
        })

        return context


class BlogListView(generic.ListView):
    model = Blog


class BloggerListView(generic.ListView):
    model = User


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post.html'

    def get_object(self, **kwargs):
        """Override get_object() method to return the correct post. Needed b/c we use two args in the url."""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post


class BlogDetailView(generic.DetailView):
    model = Blog