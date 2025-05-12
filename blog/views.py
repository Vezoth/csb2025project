from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import BlogPost, Comment
from django.contrib.auth import logout, login, authenticate

# Create your views here.
def index(request):
    posts = BlogPost.objects.all().order_by('-created')
    return render(request, 'blog/index.html', {'posts' : posts})

def logout_view(request):
    logout(request)
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'blog/login.html', {'error' : 'Invalid username or password.'})
    return render(request, 'blog/login.html')

def blogpost_view(request, blogpk):
    blogpost = get_object_or_404(BlogPost, pk=blogpk)
    comments = Comment.objects.filter(post=blogpost)
    return render(request, 'blog/blogpost.html', {'blogpost' : blogpost, 'comments' : comments})