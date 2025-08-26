from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,permission_required
from . import forms as fm 
from .models import Post, PostLike,Comment, Category
from django.contrib.auth import get_user_model
from django.views.generic import FormView, ListView, DetailView 
from django.views.generic.edit import FormMixin

from django.urls import reverse_lazy 
from django.utils.decorators import method_decorator

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import CommentForm,ContactForm
from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden

# Create your views here.



# class AddingPost(CreateView):
#     template_name="post/add-post.html"
#     success_url = reverse_lazy('my-post')

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))




# super user lai matra access diney partt 
class SuperUserRequiredMixin( LoginRequiredMixin ,UserPassesTestMixin):
   
   def test_func(self):
        return self.request.user.is_superuser
    

   def handle_no_permission(self):
        if self.request.user.is_authenticated:
         return HttpResponseForbidden('You are not authorised to acces this page')
        return super().handle_no_permission()
    


from .models import Notification
from django.contrib.auth import get_user_model

#adding posts 
@login_required
# @user_passes_test(lambda u: u.is_staff)
@staff_member_required


def add_post(request):
    if request.method == 'POST':
        form = fm.PostForm(request.POST, request.FILES)
        if form.is_valid():
            var = form.save(commit=False)
            var.author = request.user
            var.save()
            messages.success(request, 'Post has been created')

            # --- Notification logic starts here ---
            # Get all staff users except the one who created the post

            # User = get_user_model()

            # other_staff_users = User.objects.filter(is_superuser=True)

            # # Create notifications for each staff user
            # for user in other_staff_users:
            #     Notification.objects.create(
            #         user=user,
            #         message=f"New post titled '{var.title}' created by '{request.user.username}'"
            #     )

            # --- Notification logic ends here ---

            if request.user.is_superuser:
                return redirect('admin_post')
            return redirect('my_post')

        else:
            messages.warning(request, 'Post was not able to be created')
            return redirect('add-post')
    else:
        form = fm.PostForm()
        context = {'form': form, 'is_author': request.user.groups.filter(name='author').exists()}
    return render(request, 'dashboard/posts/add_post.html', context)


#updating posts 
@login_required
@staff_member_required

def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    User = get_user_model()

    
    if not (request.user == post.author or request.user.is_superuser):
        return HttpResponseForbidden('You are not authorised')

    if request.method == 'POST':
        form = fm.PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            
            # Send notifications to other staff users
            superusers=User.objects.filter(is_superuser=True)
            editor=request.user

            for admin in superusers:
                Notification.objects.create(
                    user=admin,
                    message=f" Post '{post.title}' has been updated by {editor.username}",
                    model_name="post.Post",
                    model_id=post.id

                )

            if post.author not in superusers:
                Notification.objects.create(
                    user=post.author,

                    #  yo use garna mildaina kna bhaney yesle post ko author lai access gana sakidaina so use this in update_post ma 
                    message=f" Post '{post.title}' has been updated by {editor.username}",
                    model_name="post.Post",
                    model_id=post.id

#             )

            )
                
            messages.success(request, 'Post updated successfully ')
            
            if request.user.is_superuser:
                return redirect('admin_post')
            else:
                return redirect('my_post')
        else:
            messages.warning(request, 'Unable to update post. Please check the form.')
            return redirect('update-post', pk=post.pk)
    
    else:
        form = fm.PostForm(instance=post)

    context = {'form': form, 'post': post}
    return render(request, 'dashboard/posts/add_post.html', context)
    


    


# deleting posts
@login_required
@staff_member_required

def delete_post(request,pk):
    post= Post.objects.get(pk=pk)
    
    if  not (request.user == post.author or request.user.is_superuser):
        raise PermissionDenied
    
    else: 
        post.delete()

        messages.success(request,"Post deleted")
        return redirect('admin_post')



#post details
def post_details(request,pk):
    post = Post.objects.get(pk=pk)
    likecount= PostLike.objects.filter(post=post).count()
    comments = post.comments.filter(parents__isnull=True, is_delete=False).order_by('-date_posted')
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
  



#author posts
@login_required
@staff_member_required
def author_posts(request,pk):
   author = get_user_model().objects.get(pk=pk)
   posts = Post.objects.filter(author=author, is_draft='False')
#    breakpoint()
  
   context ={ 'author':author, 'posts': posts}
   return render (request, 'post/author_post.html',context)



from django.core.paginator import Paginator



# def my_post(request):
#     post = Post.objects.filter(author=request.user, author__is_staff=True).order_by('-date_posted')
#     paginator = Paginator(post, 10)  # Show 10 contacts per page.
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'posts': post,
#         'page_obj': page_obj
#     }
#     return render(request, 'dashboard/posts/my_post.html', context)

class AuthorPostView(ListView, ):

    model= Post
    template_name="dashboard/posts/my_post.html"
    paginate_by=10
    context_object_name='posts'

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user ).order_by('-date_posted')
    




from accounts.models import User 
# # like posts 
@login_required

def like_post(request, pk):
    post = Post.objects.get(pk=pk) 
    post_like_qs = PostLike.objects.filter(post=post, reader=request.user)

    if post_like_qs.exists():
        # Since user already liked, just show warning and redirect
        messages.warning(request, "Already liked")
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin_post_details', post.pk )
        else:
            return redirect('post-details', post.pk)
    else:
        # Create new like entry
        PostLike.objects.create(reader=request.user, post=post, like_count=1)
        messages.success(request, "Post liked")


        superusers=User.objects.filter(is_superuser=True)

        for admin in superusers:
            Notification.objects.create(
                user=admin,
                message=f"{request.user.username} liked the post: '{post.title}'", 
                model_name="post.Post",
                model_id=post.id
            )

        if post.author not in superusers:
            Notification.objects.create(
                    user=post.author,
                    message=f"{request.user.username} liked your post: '{post.title}'",
                    model_name="post.Post",
                    model_id= post.id
                )

        if request.user.is_superuser or request.user.is_staff:
             return redirect('admin_post_details', post.pk )
        
        else:
            return redirect('post-details', post.pk)



@login_required 
def post_likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes_qs = PostLike.objects.filter(post=post).select_related('reader')

    likes = [{'username': like.reader.username} for like in likes_qs]

    return JsonResponse({'likes': likes})


from django.db.models import Count,Q

# show all trending  post from db is the post is not draft 
def all_posts(request):
    is_author = False

    if request.user.is_authenticated:
        is_author = request.user.groups.filter(name='author').exists()

    posts = Post.objects.filter(is_draft=False).order_by('-date_posted')
    categories = Category.objects.all()
    posts = posts.annotate(comment_count=Count('comments', filter=Q(comments__is_delete=False)))
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
        return 
   

#  to get category posts


class CategoryPostsView(ListView):
    model = Post
    template_name = 'post/category_posts.html'  # your template
    context_object_name = 'posts'

    def get_queryset(self):
        category_pk = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_pk)
        return Post.objects.filter(category=category, is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return context
    

class AuthorPostViewforUser(ListView):
    model=Post
    template_name='post/author_posts.html'
    context_object_name='posts'

    def get_queryset(self):
        author_pk=self.kwargs.get('pk')
        author=get_object_or_404(get_user_model(), pk=author_pk)
        return Post.objects.filter(author=author,is_draft=False).order_by('date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return context

    



class AdminPostView(SuperUserRequiredMixin, ListView):
    
    template_name='dashboard/posts/list_posts.html'
    paginate_by=10  # aauta page ma kati ota post dekhauney 

    model=Post 
    context_object_name = 'posts'
    queryset=Post.objects.all().order_by('-date_posted')

   



class CommentListView(SuperUserRequiredMixin, ListView):
    template_name='dashboard/comments/admin_comments_list.html'
    model=Comment
    context_object_name='comments'
    paginate_by=10

    def get_queryset(self):
        return Comment.objects.all().select_related('post','author').order_by('-date_posted')
    



# @method_decorator(staff_member_required, name='dispatch')

class AdminPostDetailsView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    template_name = 'dashboard/posts/admin_post_details.html'
    model = Post
    context_object_name = 'post'
    form_class = CommentForm  # needed by FormMixin

    

    def test_func(self):
     return self.request.user.is_superuser or self.request.user.is_staff
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
         return HttpResponseForbidden('You are not authorised to acces this page')
        return super().handle_no_permission()
    

    def get_success_url(self):
        return self.request.path  # reload same page after POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['like_count'] = PostLike.objects.filter(post=post).count()
        context['comments'] = post.comments.filter(parents__isnull=True, is_delete=False).order_by('-date_posted')
        context['form'] = kwargs.get('form') or self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # required for DetailView
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to comment")
            return redirect('login')

        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object

            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parents_id = int(parent_id)

            comment.save()
            return redirect(self.get_success_url())

        # If form is invalid, re-render page with errors
        return self.render_to_response(self.get_context_data(form=form))    






class SearchPostView(ListView):

    model=Post
    template_name= 'dashboard/posts/search_posts.html'
    context_object_name= 'posts'

    def get_queryset(self):
        queryset = Post.objects.all()
        search_query = self.request.GET.get('search', '').strip()
        content_type = self.request.GET.get('content_type', '').strip()

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('search', '').strip()
        
        return context
    




from django.views import View
class MarkAllNorificationRead(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})




from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from .models import Notification  # adjust as per your project structure
from django.apps import apps

def notificationDetailView(request, pk):
    notification=get_object_or_404(Notification, pk=pk, user=request.user)
    model_class= get_model_from_string(notification.model_name)
    model_id=notification.model_id

    if not model_class:
        return HttpResponseNotFound('Model not found')
    
    try:
        model_instance = model_class.objects.get(id=model_id)

        # notification = Notification.objects.get(id=pk)
    except model_class.DoesNotExist:
        return HttpResponseNotFound('Notification not found')

    print('noti', notification.model_name)

    # Fetch model class from string
    # model_class = get_model_from_string(notification.model_name)
    # model_id = notification.model_id
    # print('model', model_class)

    # if not model_class:
    #     return HttpResponseNotFound('Model not found')

    # try:
    #     model_instance = model_class.objects.get(id=model_id)
    # except model_class.DoesNotExist:
    #     return HttpResponseNotFound('Model instance not found')

    notification.is_read = True
    notification.save()

    if hasattr(model_instance, "get_absolute_url"):
        return redirect(model_instance.get_absolute_url())
    else:
        return HttpResponseNotFound('Details view not found')



from django.apps import apps

def get_model_from_string(model_string):
    """
    Expects model_string in the format 'app_label.ModelName'
    Example: 'post.Category'
    """
    try:
        app_label, model_name = model_string.split(".")
        return apps.get_model(app_label=app_label, model_name=model_name)
    except Exception as e:
        print(f"Model resolution error: {e}")
        return None


#  this is for the superadmin to edit any comment
from django.views.generic.edit import UpdateView
class EditCommentView(SuperUserRequiredMixin, UpdateView ):
    model=Comment
    template_name='dashboard/comments/edit_comments.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('admin_post_details', kwargs={'pk': self.object.post.pk})
    

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.save()
        
        messages.success(self.request, 'Comment updated successfully')
        return super().form_valid(form)


#  this is for user to edit their own comment
class EditCommentUserView(LoginRequiredMixin, UpdateView):
    model=Comment
    template_name='post/edit_comment.html'
    form_class=CommentForm
    context_object_name = 'comment'


    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.object.post.pk})

    def  form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.save()

        messages.success(self.request, 'Comment updated successfully')

        return super().form_valid(form)
      


from django.views.generic.edit import DeleteView
from django.urls import reverse
class DeleteCommentUserView(LoginRequiredMixin, View):
    model=Comment
    template_name='post/delete_comment.html'
     
    def get(self, request, pk, *args, **kwargs):
        comment= get_object_or_404(Comment, pk=pk, author=request.user)
        comment.is_delete=True
        comment.save()
        messages.success(request," Comment deleted succesfuly ")

        return redirect('post-details', pk=comment.post.pk)   



# class DeleteReplyCommentUserView(LoginRequiredMixin, View):
#     def get(self, request, pk, *args, **kwargs):
#         comment = get_object_or_404(Comment, pk=pk, author=request.user)

#         if comment.parents is not None:
#             comment.is_delete = True
#             comment.save()
#             messages.success(request, "Reply deleted successfully!")
#         else:
#             messages.error(request, "You cannot delete a main comment here!")

#         return redirect('post-details', pk=comment.post.pk)


class SearchCategoryView(ListView):

    model=Category
    template_name= 'dashboard/category/search_category.html'
    context_object_name= 'categories'

    def get_queryset(self):
        queryset = Category.objects.all()
        search_query = self.request.GET.get('search', '').strip()
        content_type = self.request.GET.get('content_type', '').strip()

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('search', '').strip()
        
        return context
    

class SearchUserView(ListView):
    model=User
    template_name='dashboard/users/search_users.html'
    context_object_name='users'

    def get_queryset(self):
        queryset = User.objects.all()
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(username__icontains=search_query)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('search', '').strip()
        
        return context
    


class SearchCommentsView(ListView):
    model= Comment
    template_name='dashboard/comments/search_comments.html'
    context_object_name='comments'

    def get_queryset(self):
        queryset=Comment.objects.all()
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(content__icontains=search_query)

            return queryset
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['search_result'] = self.request.GET.get('search', '').strip()
            
            return context
            


from .models import Contact
class SearchContactView(ListView):
    model= Contact
    template_name='dashboard/contact/search_contact.html'
    context_object_name= 'contacts'

    def get_queryset(self):
        queryset=Contact.objects.all()
        search_query=self.request.GET.get('search', '').strip()

        if search_query:
            queryset= queryset.filter(name__icontains=search_query) | queryset.filter(email__icontains=search_query)

            return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('search', '').strip()
        return context




class SearchAuthorView(ListView):
    model = User
    template_name = 'dashboard/users/search_author.html'
    context_object_name = 'authors'

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=True)
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(username__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('search', '').strip()
        return context
        

class SearchAuthorPostView(ListView):
    model = Post
    template_name = 'dashboard/posts/search_mypost.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        search_query = self.request.GET.get('search', '').strip()

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.request.GET.get('search', '').strip()
        return context
    
# @login_required

# def softDeleteCommentByUser(request,pk):
    
#     comment=Comment.objects.get(id=pk)
#     context= { 'comments': comment}

#     if request.method == 'POST':
#         comment.is_delete=True
#         comment.save()
#         messages.success(request,'Comment deleted successfully')
#         return redirect('admin_comment_list')
    
    
#     return render(request,'dashboard/comments/delete_comments.html', context)
