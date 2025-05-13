from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import BlogPost, Comment
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = BlogPost.objects.all().order_by('-created')
    return render(request, 'blog/index.html', {'posts' : posts})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')



def blogpost_view(request, blogpk):
    blogpost = get_object_or_404(BlogPost, pk=blogpk)
    comments = Comment.objects.filter(post=blogpost)
    return render(request, 'blog/blogpost.html', {'blogpost' : blogpost, 'comments' : comments})

@login_required
def deletepost(request, blogpk):
    blogpost = get_object_or_404(BlogPost, pk=blogpk)
    
    if request.user != blogpost.author:
        return redirect('/')
    
    blogpost.delete()

    return redirect('/')

@login_required
def editpost(request, blogpk):
    blogpost = get_object_or_404(BlogPost, pk=blogpk)

    # if request.user != blogpost.author:
    #     redirect('/')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        
        blogpost.title = title
        blogpost.content = content
        blogpost.save()
        return redirect('postview', blogpk=blogpost.pk)

    return render(request, 'blog/neweditblog.html', {'blogpost' : blogpost})

@login_required
def newpost(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']  
        blogpost = BlogPost(title=title, content=content, author=request.user)
        blogpost.save()
        return redirect('postview', blogpk=blogpost.pk)
    return render(request, 'blog/neweditblog.html')

@login_required
def deletecomment(request, blogpk, commentpk):
    return redirect('/')
