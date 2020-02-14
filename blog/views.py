from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.forms import ModelForm

from blog.models import Blog, Post, Comment
from blog.forms import RegistrationForm, CommentForm
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
            'title': 'index',
        })

        return context


class BlogListView(generic.ListView):
    """List view for displaying all the blogs."""
    model = Blog
    template_name = 'blog_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'blogs'
        })
        return context


class UserListView(generic.ListView):
    """List view of all the users."""
    model = User
    template_name = 'user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'users'
        })
        return context

class UserDetailView(generic.DetailView):
    """Detail view for an individual user."""
    model = User
    template_name = 'user_detail.html'

    def get_object(self, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': self.request.user.username,
        })
        return context


class PostListView(generic.ListView):
    """List view of all posts across."""
    model = Post
    template_name = 'post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'all posts'
        })
        return context


class PostDetailView(generic.DetailView):
    """Detail view for an individual post, also displays comments on the post.
    Acts as a ListCreateView for comments by displaying the CommentForm below the comments.
    Initial values for the 'user' and 'post' field in the CommentForm are set in this view using the corresponding context data
    When the form is submitted it will post to the CommentCreateView which only accepts POST requests """
    model = Post
    template_name = 'post_detail.html'

    def get_object(self, **kwargs):
        """Override get_object() method to return the correct post. Needed b/c of "view must be called with either an object pk or a slug in the urlconf" error."""
        self.post = get_object_or_404(Post, pk=self.kwargs['post_pk']) # Set post as an instance variable because it is used in get_context_data to pass the post to the CommentForm
        return self.post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial = {
            'post': self.post,
            'user': self.request.user,
        }
        context.update({
            'form': CommentForm(initial=initial),
            'title': self.post.title,
        })
        return context

class CommentCreateView(generic.edit.FormView):
    """View used to create comments on Posts.
    Redirects to PostDetail view with list of comments"""
    form_class = CommentForm

    def form_valid(self, form):
        self.comment = form.save()
        return super().form_valid(form)

    def get_success_url(self): 
        return reverse('post-detail', kwargs={'blog_pk': self.comment.post.blog.id, 'post_pk': self.comment.post.id})



class BlogDetailView(generic.DetailView):
    """Detail view of a single blog, displays all posts ordered by their posted date."""
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self, **kwargs):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['blog_pk'])
        return self.blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': self.blog.name
        })
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'register'
        })
        return context


class PostCreateView(generic.edit.CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = ['title', 'body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'create post'
        })
        return context

    def form_valid(self, form):
        self.post = form.save(commit=False)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title': 'create blog'
        })
        return context

    def form_valid(self, form):
        self.blog = form.save(commit=False) # Create instance of the blog, but don't save to database becuase we have to set the user which is done in the next line
        self.blog.user = self.request.user
        self.blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'blog_pk': self.blog.id})