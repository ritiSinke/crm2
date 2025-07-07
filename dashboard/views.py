from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from post.models import Post 

# Create your views here.


@login_required
def dashboard(request):
     return redirect('all-posts')
  