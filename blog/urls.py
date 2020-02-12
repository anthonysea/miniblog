from django.urls import path
from . import views
from django.views.decorators.http import require_POST

#app_name = 'blog'

# Index and List views of Blogs, Users, and Posts
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
]

urlpatterns += [
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
]

# Detail views of Users, Blogs, and Posts
urlpatterns += [
    path('user/<int:user_pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('blog/<int:blog_pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<int:blog_pk>/post/<int:post_pk>', views.PostDetailView.as_view(), name='post-detail'),
]

# Create views for Post and Blog
urlpatterns += [
    path('blogs/create', views.BlogCreateView.as_view(), name='blog-create'),
    path('posts/create', views.PostCreateView.as_view(), name='post-create'),
    path('comments/create', require_POST(views.CommentCreateView.as_view()), name='comment-create')
]