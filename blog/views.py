from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse

from blog.models import Blog, Post, Comment
from blog.forms import RegistrationForm
from django.contrib.auth.models import User

from datetime import date

class IndexView(generic.TemplateView):
    """Index view to display basic statistics of the website. Makes use of overriding the get_context_data method of superclass."""
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        """Override get_context_data() to be able to add additional items in the context dict to be available on the template"""
        context = super().get_context_data(**kwargs) # Need to call and set using parent method first

        num_blogs = Blog.objects.all().count()
        num_users = User.objects.all().count() - 1
        num_posts = Post.objects.all().count()
        try:
            latest_post = Post.objects.latest('posted_on')
        except Post.DoesNotExist:
            latest_post = None

        context.update({
            'num_blogs': num_blogs,
            'num_users': num_users,
            'num_posts': num_posts,
            'latest_post': latest_post,
        })

        return context


class BlogListView(generic.ListView):
    """List view for displaying all the blogs."""
    model = Blog
    template_name = 'blog_list.html'


class UserListView(generic.ListView):
    """List view of all the users."""
    model = User
    template_name = 'user_list.html'

class UserDetailView(generic.DetailView):
    """Detail view for an individual user."""
    model = User
    template_name = 'user_detail.html'

    def get_object(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return user


class PostListView(generic.ListView):
    """List view of all posts across."""
    model = Post
    template_name = 'post_list.html'


class PostDetailView(generic.DetailView):
    """Detail view for an individual post, also displays comments on the post."""
    model = Post
    template_name = 'post_detail.html'

    def get_object(self, **kwargs):
        """Override get_object() method to return the correct post. Needed b/c of "view must be called with either an object pk or a slug in the urlconf" error."""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return post


class BlogDetailView(generic.DetailView):
    """Detail view of a single blog, displays all posts ordered by their posted date."""
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self, **kwargs):
        blog = get_object_or_404(Blog, pk=self.kwargs['blog_pk'])
        return blog

class RegisterView(generic.edit.FormView):
    """Simple view that displays the RegistrationForm for registering to use the website."""
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    #success_url = 'blog:index'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user), 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class PostCreateView(generic.edit.CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'body']

    def form_valid(self, form):
        self.post = form.save()
        self.post.author = User.objects.get(id=self.request.user.id)
        self.post.blog = Blog.objects.get(user=self.request.user.id)
        self.post.posted_on = date.today()
        self.post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'blog_pk': self.post.blog.id, 'post_pk': self.post.id})


class BlogCreateView(generic.edit.CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ['name']