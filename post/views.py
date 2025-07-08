from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,permission_required
from . import forms as fm 
from .models import Post, PostLike,Comment, Category
from django.contrib.auth import get_user_model
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy 
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import CommentForm,ContactForm
# Create your views here.



# class AddingPost(CreateView):
#     template_name="post/add-post.html"
#     success_url = reverse_lazy('my-post')

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))

#adding posts 
@login_required
# @user_passes_test(lambda u: u.is_staff)
# @staff_member_required
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
            return redirect( 'admin_posts')
 
        else:

            messages.warning (request,'Post was not able to be created')
            return redirect ('add-post')
    else:
        form = fm.PostForm()
        context ={ 'form':form, 'is_author': request.user.groups.filter(name='author').exists()}
    return render(request,'post/add_post.html', context)
    

#updating posts 
@login_required
def update_post(request,pk):
    post = Post.objects.get(pk=pk)

  
    if request.method == 'POST':
        form = fm.PostForm(request.POST,request.FILES, instance=post)

        if form.is_valid():
    
            form.save()
            messages.success(request,'Post updated')
            return redirect ('admin_post')
        else:
            messages.warning(request, 'Post unable to update')
            return redirect('update-post', post.pk)
        
    else:
        form =fm.PostForm(instance=post)
        context ={ 'form' : form, 'post': post, 'is_author': request.user.groups.filter(name='author').exists()}
    return render(request,'post/add_post.html',context)
    


# deleting posts
@login_required
def delete_post(request,pk):
    post= Post.objects.get(pk=pk)

    
    
    post.delete()
    messages.success(request,"Post deleted")
    return redirect('admin_post')



#post details
def post_details(request,pk):
    post = Post.objects.get(pk=pk)
    likecount= PostLike.objects.filter(post=post).count()
    comments = post.comments.filter(parents__isnull=True).order_by('-date_posted')
    form=CommentForm()


   
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user  # This sets the comment's author to the logged-in user

                comment.post = post

                parent_id = request.POST.get('parent_id')
                if parent_id:
                     comment.parents_id= int (parent_id)

                comment.save()
                print(form.errors)
                return redirect('post-details', pk=post.pk)
            else:
           
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

def like_post(request, pk):
    post = Post.objects.get(pk=pk) 
    post_like_qs = PostLike.objects.filter(post=post, reader=request.user)

    if post_like_qs.exists():
        # Since user already liked, just show warning and redirect
        messages.warning(request, "Already liked")
        return redirect('post-details', post.pk)
    else:
        # Create new like entry
        PostLike.objects.create(reader=request.user, post=post, like_count=1)
        messages.success(request, "Post liked")
        return redirect('post-details', post.pk)



@login_required 
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

    from django.db.models import Count
    posts = Post.objects.filter(is_draft=False).order_by('-date_posted')
    categories = Category.objects.all()
    posts = posts.annotate(comment_count=Count('comments'))
    trending_posts = Post.objects.filter(is_draft=False) \
                        .annotate(num_comments=Count('comments')) \
                        .filter(num_comments__gt=0) \
                        .order_by('-num_comments')[:5]

    return render(request, 'post/all_posts.html', {
        'posts': posts,
        'is_author': is_author,
        'categories' : categories,
        'trending_posts': trending_posts
    })




   


# searching posts 
def search_posts(request):
    query = request.GET.get('q', '').strip()  # default to empty string and strip whitespace
    

    if query:
        posts = Post.objects.filter(title__icontains=query)

    context = {'query': query, 'posts': posts}

    return render(request, 'post/search_posts.html', context)  


# contact page viewing 
class ContactView(FormView):
    template_name = 'post/staticPages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
       
       self.object = form.save()
       messages.success(self.request, "Your message has been sent successfully!")
       return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "There was an error sending your message. Please try again.")
        return super().form_invalid(form)
   

#  to get category posts
class CategoryPostsView(ListView):
    model = Post
    template_name = 'post/category_posts.html'  # your template
    context_object_name = 'posts'
    paginate_by = 10  # optional, if you want pagination

    def get_queryset(self):
        category_pk = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_pk)
        return Post.objects.filter(category=category, is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return context
    




class AdminPostView(ListView):

    template_name='dashboard/list_posts.html'
    model=Post 
    context_object_name = 'posts'

    def get_queryset(self):
        
        return Post.objects.filter(is_draft=False).order_by('-date_posted')

    



    
