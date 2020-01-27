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
        num_users = User.objects.all().count() - 1
        num_posts = Post.objects.all().count()
        latest_post = Post.objects.latest('posted_on')

        context.update({
            'num_blogs': num_blogs,
            'num_users': num_users,
            'num_posts': num_posts,
            'latest_post': latest_post,
        })

        return context


class BlogListView(generic.ListView):
    model = Blog
    template_name = 'blog_list.html'


class UserListView(generic.ListView):
    model = User
    template_name = 'user_list.html'

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'user_detail.html'

    def get_object(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return user


class PostListView(generic.ListView):
    model = Post
    template_name = 'post_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_object(self, **kwargs):
        """Override get_object() method to return the correct post. Needed b/c of "view must be called with either an object pk or a slug in the urlconf" error."""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name='blog_detail.html'

    def get_object(self, **kwargs):
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_pk'])
        return blog