from .models import Blog
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogSerializer
from django.db.models import Q

# Create your views here.
@api_view(["POST", "GET"])
def blog_list(request):
    term = request.GET.get("term", "")

    if request.method == "GET":
        if term:
            blogs = Blog.objects.filter(Q(title__icontains=term) | Q(content__icontains=term) | Q(category__icontains=term))
        else:
            blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def blog_search(request, term):
    if request.method == "GET":
        blog = Blog.objects.filter(Q(title__contains=term) | Q(content__contains=term) | Q(category__contains=term))
        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_204_NO_CONTENT)