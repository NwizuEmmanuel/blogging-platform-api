from rest_framework.test import APITestCase
from rest_framework import status
from .models import Blog
from django.urls import reverse

class BlogAPITests(APITestCase):
    def setUp(self):
        """Set up initial data for tests."""
        self.blog_data = {
            "title": "Test Blog",
            "content": "This is a test content.",
            "category": "test category",
            "tags": "tag1,tag2"
        }
        self.blog = Blog.objects.create(**self.blog_data)
        self.url = reverse("blog-list")
    
    def test_create_blog(self):
        """Test creating new blog via api"""
        response = self.client.post(self.url, self.blog_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.blog_data["title"])
        self.assertEqual(response.data["content"], self.blog_data["content"])
        

# Create your tests here.
