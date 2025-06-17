from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from . import forms as fm 
from .models import Post, PostLike, Category
from django.contrib.auth import get_user_model
# Create your views here.

#adding posts 
@login_required
def add_post(request):

    if request.method == 'POST':
        form = fm.AddPostForm(request.POST,request.FILES)
        print(f"Files: {request.FILES}")  
        if form.is_valid():
            var= form.save(commit= False)
            var.author= request.user

            print(f"Files: {request.FILES}")  
            var.save()
            messages.success(request,'Post has been created')
            return redirect( 'my-post')
 
        else:

            messages.warning (request,'Post was not able to be created')
            return redirect ('add-post')
    else:
        form = fm.AddPostForm()
        context ={ 'form':form}
    return render(request,'post/add_post.html', context)
    

#updating posts 
@login_required
def update_post(request,pk):
    post = Post.objects.get(pk=pk)

    if not post.author == request.user:
        messages.warning(request,"Permission denied")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = fm.UpdatePostForm(request.POST,request.FILES, instance=post)

        if form.is_valid():
    
            form.save()
            messages.success(request,'Post updated')
            return redirect ('my-post')
        else:
            messages.warning(request, 'Post unable to update')
            return redirect('update-post', post.pk)
        
    else:
        form =fm.UpdatePostForm(instance=post)
        context ={ 'form' : form, 'post': post}
    return render(request,'post/update_post.html',context)
    

#post details
def post_details(request,pk):
    post = Post.objects.get(pk=pk)

    context ={ 'post': post,}
    return render (request, 'post/post_details.html',context)

#author posts
def author_posts(request,pk):
   author = get_user_model().objects.get(pk=pk)
   posts = Post.objects.filter(author=author, is_draft='False')
#    breakpoint()
  
   context ={ 'author':author, 'posts': posts}
   return render (request, 'post/author_post.html',context)



# deleting posts
@login_required
def delete_post(request,pk):
    post= Post.objects.get(pk=pk)

    if not post.author == request.user:
        messages.warning(request,"Permission denied")
        return redirect('dashboard')
    
    post.delete()
    messages.success(request,"Post deleted")
    return redirect('my-post')


@login_required
def my_post(request):
    post= Post.objects.filter(author=request.user)
    context ={ 'post': post}
    return render(request, 'post/my_post.html', context)







# # like posts 
# @login_required
# def like_post(request,pk):

#     post = Post.objects.get(pk=pk) 
#     post_like_qs= PostLike.objects.filter(post=post, reader=request.user)

#     if post_like_qs.exists():
#         post_like=post_like_qs.first()
#         if  post_like.reader == request.user:
#           messages.warning(request,"Already iked")
#           return redirect('post-details',post.pk)

#         post_like.like_count= post_like.like_count + 1 
#         post_like.save()
#         messages.success(request,"Post liked")
#         return  redirect('post-details',post.pk)                           
#     else:
#         PostLike.objects.create(reader=request.user, post=post, like_count=1)
#         messages.success(request,"Post liked")
#         return  redirect('post-details',post.pk)





def all_posts(request):
    posts = Post.objects.filter(is_draft='False').order_by('-date_posted')      # Get all posts, newest first

    # .order_by('-date_posted')
    return render(request, 'post/all_posts.html', {'post': posts})

