from django.urls import path, include
from . import views

urlpatterns = [
    path("blogs/", views.blog_list, name="blog-list"),
    path("blogs/<int:pk>/", views.blog_detail, name="blog-detail"),
]
