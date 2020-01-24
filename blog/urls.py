from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
]

urlpatterns += [
    path('postz/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('blogz/<int:pk>', views.BlogDetailView.as_view(), name='blog'),
]