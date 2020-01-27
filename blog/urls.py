from django.urls import path
from . import views

# Index and List views of Blogs, Users, and Posts
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
]

# Detail views of Users, Blogs, and Posts
urlpatterns += [
    path('user/<int:user_pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('blog/<int:blog_pk>', views.BlogDetailView.as_view(), name='blog'),
    path('blog/<int:blog_pk>/post/<int:post_pk>', views.PostDetailView.as_view(), name='post-detail'),
]