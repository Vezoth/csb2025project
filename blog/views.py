from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import BlogPost, Comment
from django.db import connection
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.
def index(request):
    search = request.GET.get('search', '')
    if search:
        query = "SELECT title, author_id, created, id FROM blog_blogpost WHERE title LIKE '%%%s%%' ORDER BY created DESC" % search
        with connection.cursor() as cursor:
            cursor.execute(query)
            posts = [{'title' : row[0],
                      'author_id' : row[1],
                      'created' : row[2],
                      'pk' : row[3]} 
                      for row in cursor.fetchall()]
            for post in posts:
                post['author'] = User.objects.get(pk=post['author_id'])
        # query = "SELECT id FROM blog_blogpost WHERE title LIKE %s ORDER BY created DESC"
        # posts = BlogPost.objects.raw(query, [f"%{query}%"])
        #### OR ####
        # posts = BlogPost.objects.filter(title__icontains=search).order_by('-created')
    else:
        posts = BlogPost.objects.all().order_by('-created')
    return render(request, 'blog/index.html', {'posts' : posts})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def settings(request):
    if request.method == 'POST':
        # oldpassword = request.POST.get('oldpassword', '')
        # if not request.user.check_password(oldpassword):
        #    return render(request, 'blog/usersettings.html', {'error': 'Old password is incorrect.'})
        newpassword = request.POST.get('newpassword', '')
        if not newpassword:
            return render(request, 'blog/usersettings.html', {'error' : 'New password is invalid.'})
        try:
            validate_password(newpassword)
        except ValidationError as e:
            return render(request, 'blog/usersettings.html', {'error': e.messages})
        user = request.user
        user.set_password(newpassword)
        user.save()
        return render(request, 'blog/usersettings.html', {'msg' : 'Password has bee updated.'})
    return render(request, 'blog/usersettings.html')

def register(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        passwordcheck = request.POST.get('passwordcheck', '')
        username = request.POST.get('username', '')

        context = {
            'username' : username,
            'password' : password,
            'passwordcheck' : passwordcheck,
            'error' : []
        }
        if password != passwordcheck:
            context['error'].append('Passwords do not match.')
        try:
            validate_password(password)
        except ValidationError as e:
            for msg in e.messages:
                context['error'].append(msg)
        
        if User.objects.filter(username=username).exists():
            context['error'].append('Username already taken.')
        
        if context['error']:
            return render(request, 'blog/register.html', context)

        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return redirect('/')

    return render(request, 'blog/register.html')

def blogpost_view(request, blogpk):
    blogpost = get_object_or_404(BlogPost, pk=blogpk)
    comments = Comment.objects.filter(post=blogpost)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            render(request, 'blog/blogpost.html', {'blogpost' : blogpost, 'comments' : comments})
        content = request.POST.get('comment')
        if not content:
            render(request, 'blog/blogpost.html', {'blogpost' : blogpost, 'comments' : comments})
        comment = Comment(
            author=request.user,
            post=blogpost,
            content=content)
        comment.save()
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
    errors = []
    blogpost = get_object_or_404(BlogPost, pk=blogpk)

    # if request.user != blogpost.author:
    #     raise PermissionDenied

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        
        blogpost.title = title
        blogpost.content = content
        errors = problems_in_blog(blogpost)
        if not errors:
            blogpost.save()
            return redirect('postview', blogpk=blogpost.pk)

    return render(request, 'blog/neweditblog.html', {'blogpost' : blogpost, 'errors' : errors})

@login_required
def newpost(request):
    errors = []
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content'] 
        blogpost = BlogPost(title=title, content=content, author=request.user)
        # errors = problems_in_blog(blogpost)
        # if not errors:
        #     blogpost.save()
        #     return redirect('postview', blogpk=blogpost.pk)
        blogpost.save()
        return redirect('postview', blogpk=blogpost.pk)
    return render(request, 'blog/neweditblog.html', {'errors' : errors})

@login_required
def deletecomment(request, blogpk):
    blogpost = get_object_or_404(BlogPost, pk=blogpk)
    commentpk = request.GET.get('delc')
    comment = get_object_or_404(Comment, pk=commentpk)
    if request.user != comment.author:
        raise PermissionDenied
    confirm = request.GET.get('confirm')
    print(commentpk)
    print(confirm)
    if confirm is not None:
        comment.delete()
        print("here")
        return redirect('postview', blogpk=blogpk)

    return render(request, 'blog/confirmdelete.html', {'blogpost': blogpost, 'comment' : comment})


def problems_in_blog(blog):
    errors = []
    if len(blog.title) < 3:
        errors.append('Title must be at least 3 characters.')
    if len(blog.content) < 10:
        errors.append('Content must be at least 10 characters')
    return errors