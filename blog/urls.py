from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog/blogs/', views.AllBlogsView.as_view(), name='blogs'),
    path('blogger/bloggers/', views.AllBloggersView.as_view(), name='bloggers'),
]

urlpatterns += [
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
]