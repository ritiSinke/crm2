from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from post.models import Post 

# Create your views here.


@login_required
def dashboard(request):
    is_author=False

    if not request.user.groups.filter(name='author').exists():
        return redirect('all-posts')
    return render(request, 'dashboard/dashboard.html',{
        'is_author': is_author
    })