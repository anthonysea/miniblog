from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
]

urlpatterns += [
    path('blog/<int:blog_pk>/post/<int:post_pk>', views.PostDetailView.as_view(), name='post'),
    path('blog/<int:blog_pk>', views.BlogDetailView.as_view(), name='blog'),
]