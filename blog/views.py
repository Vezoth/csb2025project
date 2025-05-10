from django.shortcuts import render
from .models import BlogPost, Comment

# Create your views here.
def index(request):
    posts = BlogPost.objects.all().order_by('-created')
    return render(request, 'blog/index.html', {'posts' : posts})