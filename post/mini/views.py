from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .models import Blog

def home(request):
    posts =  Blog.objects.only('id', 'title', 'desc')
    return render(request, 'home.html', {'post': posts})

def post_detail(request, id):
    post = Blog.objects.get(pk=id)
    return render(request, 'post_detail.html', {'post': post})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        user = Blog.objects.all()
        return render(request, 'dashboard.html', {'users': user})
    else:
        return HttpResponseRedirect('/login/')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if not request.user.is_authenticated: 
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def user_logout(request):  
    logout(request)  
    return HttpResponseRedirect('/')

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:  
            form = PostForm()       
        return render(request, 'addpost.html', {'form': form}) 
    else:
        return HttpResponseRedirect('/login/')
        
def update_post(request, id):
    if request.user.is_authenticated:
        pi = Blog.objects.get(pk=id)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm(instance=pi)        
        return render(request, 'updatepost.html', {'form': form}) 
    else:
        return HttpResponseRedirect('/dashboard/')
    
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Blog.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
