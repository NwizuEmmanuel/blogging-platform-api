from rest_framework.test import APITestCase
from rest_framework import status
from .models import Blog
from django.urls import reverse

# Create your tests here.
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
    
    def test_get_blog(self):
        """Test for get all blog"""
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.blog_data["title"])
        self.assertEqual(response.data[0]["content"], self.blog_data["content"])
    
    def test_get_single_blog(self):
        """Test for getting single blog by ID"""
        blog_url = reverse("blog-detail", args=[self.blog.id])
        response = self.client.get(blog_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.blog_data["title"])
        self.assertEqual(response.data["content"], self.blog_data["content"])
    
    def test_blog_missing_fields(self):
        """Test for posting incomplete blog fields"""
        incomplete_blog_data = {
            "title": "Incomplete Blog"
        }
        response = self.client.post(self.url, incomplete_blog_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("content", response.data)
    
    def test_filter_blog_by_term(self):
        response = self.client.get(self.url, {"term": "test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn("test", response.data[0]["title"].lower())
