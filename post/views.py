from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,permission_required
from . import forms as fm 
from .models import Post, PostLike, Category
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy 

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import CommentForm
# Create your views here.



# class AddingPost(CreateView):
#     template_name="post/add-post.html"
#     success_url = reverse_lazy('my-post')

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))

#adding posts 
@login_required
@permission_required("post.add_post","all-posts")
def add_post(request):

    if request.method == 'POST':
        form = fm.PostForm(request.POST,request.FILES)
        # print(f"Files: {request.FILES}")  
        if form.is_valid():
            var= form.save(commit= False)
            var.author= request.user

            # print(f"Files: {request.FILES}")  
            var.save()
            messages.success(request,'Post has been created')
            return redirect( 'my-post')
 
        else:

            messages.warning (request,'Post was not able to be created')
            return redirect ('add-post')
    else:
        form = fm.PostForm()
        context ={ 'form':form, 'is_author': request.user.groups.filter(name='author').exists()}
    return render(request,'post/add_post.html', context)
    

#updating posts 
@login_required
@permission_required("post.change_post","all-posts")
def update_post(request,pk):
    post = Post.objects.get(pk=pk)

    if not post.author == request.user:
        messages.warning(request,"Permission denied")
        return redirect('my-post')
    

    if request.method == 'POST':
        form = fm.PostForm(request.POST,request.FILES, instance=post)

        if form.is_valid():
    
            form.save()
            messages.success(request,'Post updated')
            return redirect ('my-post')
        else:
            messages.warning(request, 'Post unable to update')
            return redirect('update-post', post.pk)
        
    else:
        form =fm.PostForm(instance=post)
        context ={ 'form' : form, 'post': post, 'is_author': request.user.groups.filter(name='author').exists()}
    return render(request,'post/add_post.html',context)
    

# deleting posts
@login_required
@permission_required("post.delete_post","all-posts")
def delete_post(request,pk):
    post= Post.objects.get(pk=pk)

    if not post.author == request.user:
        messages.warning(request,"Permission denied")
        return redirect('dashboard')
    
    post.delete()
    messages.success(request,"Post deleted")
    return redirect('my-post')



#post details
def post_details(request,pk):
    post = Post.objects.get(pk=pk)
    likecount= PostLike.objects.filter(post=post).count()
    comments = post.comments.all().order_by('-date_posted')
    form=CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user  # This sets the comment's author to the logged-in user

                comment.post = post
                comment.save()
                return redirect('post-details', pk=post.pk)
            else:
            # Optionally, show a message or redirect to login
                print(form.errors)
                return redirect('login')
        else:
            form=CommentForm()
            messages.warning(request, "You must be logged in to comment")

    context = {
        'post': post,
        'comments': comments,
        'like_count': likecount,
        'form': form,
    }
    return render(request, 'post/post_details.html', context)       
    # context ={ 'post': post, 'like_count': likecount} 
    # return render (request, 'post/post_details.html',context)



#author posts
def author_posts(request,pk):
   author = get_user_model().objects.get(pk=pk)
   posts = Post.objects.filter(author=author, is_draft='False')
#    breakpoint()
  
   context ={ 'author':author, 'posts': posts}
   return render (request, 'post/author_post.html',context)




@login_required
def my_post(request):
    post= Post.objects.filter(author=request.user)
    context ={ 'post': post, 'is_author': request.user.groups.filter(name='author').exists()}
    return render(request, 'post/my_post.html', context)



# # like posts 
@login_required
def like_post(request,pk):

    post = Post.objects.get(pk=pk) 
    post_like_qs= PostLike.objects.filter(post=post, reader=request.user)

    if post_like_qs.exists():
        post_like=post_like_qs.first()
        if  post_like.reader == request.user:
          messages.warning(request,"Already liked")
          return redirect('post-details',post.pk)

        post_like.like_count= post_like.like_count + 1 
        post_like.save()
        messages.success(request,"Post liked")
        return  redirect('post-details',post.pk)                           
    else:
        PostLike.objects.create(reader=request.user, post=post, like_count=1)
        messages.success(request,"Post liked")
        return  redirect('post-details',post.pk)


@login_required 
@permission_required("post.view_postlike", "post-details")
def post_likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes_qs = PostLike.objects.filter(post=post).select_related('reader')

    likes = [{'username': like.reader.username} for like in likes_qs]

    return JsonResponse({'likes': likes})


# show all t post from db is the post is not draft 
def all_posts(request):
    is_author = False

    if request.user.is_authenticated:
        is_author = request.user.groups.filter(name='author').exists()

    posts = Post.objects.filter(is_draft=False).order_by('-date_posted')

    return render(request, 'post/all_posts.html', {
        'posts': posts,           
        'is_author': is_author    # boolean flag
    })


   


# searching posts 
def search_posts(request):
    query = request.GET.get('q', '').strip()  # default to empty string and strip whitespace
    

    if query:
        posts = Post.objects.filter(title__icontains=query)

    context = {'query': query, 'posts': posts}

    return render(request, 'post/search_posts.html', context)  
