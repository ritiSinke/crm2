from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from post.models import Post 
from django.views.generic import TemplateView,FormView,DeleteView , ListView, DetailView
from post.models import Post, Category, User, Comment 
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from post.views import SuperUserRequiredMixin
from accounts.views import StaffOrSuperuserRequiredMixin
# Create your views here.


@login_required
@staff_member_required
def dashboard(request):
    admin=False

    if request.user.is_superuser or request.user.is_staff:
        admin = True
    else:
        return redirect('all-posts')
    



    return render(request, 'dashboard/index_dashboard.html',{
        'admin': admin,
        'posts' : Post.objects.count(),
        'categories' : Category.objects.count(),
        'users' :User.objects.count(), 
        'authors' :User.objects.filter(is_staff=True).count(),
        'author_posts': Post.objects.filter(author=request.user).count(),
        
    })


from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardDetailsView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/index_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.count()
        context['categories'] = Category.objects.count()
        context['users']= User.objects.count() 
        context['authors']= User.objects.filter(is_staff=True).count()
        
        return context
 



class UserListView(SuperUserRequiredMixin, ListView):
    template_name = 'dashboard/users/user_list.html'
    paginate_by=10
    model=User
    context_object_name='users'
    queryset=User.objects.all()
    


class CategoryListView(StaffOrSuperuserRequiredMixin, TemplateView):
    template_name = 'dashboard/category/category_list.html' 
    model=Category 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    

  
    
class CategoryAddView( SuperUserRequiredMixin, FormView):
    template_name = 'dashboard/category/add_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):

        form.save()


        messages.success(self.request, 'Category added successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error adding category')
        return self.render_to_response(self.get_context_data(form=form))
    
    
class CategoryUpdateView(SuperUserRequiredMixin, FormView):
    template_name = 'dashboard/category/update_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        kwargs['instance'] = category
        return kwargs 
    
    def form_valid(self, form):

        category = form.save(commit=False)

        messages.success(self.request, 'Category Updated successfully')
        category.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error Updating category')
        return self.render_to_response(self.get_context_data(form=form))
    
    
class CategoryDeleteView(SuperUserRequiredMixin, DeleteView):

    model = Category
    template_name = 'dashboard/category_confirm_delete.html'  

   
    success_url=reverse_lazy('category_list')

    # messages.success(self.request,'User deleted successfully')
    
    


class AuthorListView(SuperUserRequiredMixin, ListView):
    template_name = 'dashboard/users/author_list.html'
    queryset=User.objects.filter(is_staff=True)
    context_object_name= 'authors'
    paginate_by=10

    
    

# class CommentUpdateView(UpdateView):

#     template_name='dashboard/delete_comments.html'
#     model=Comment
#     success_url= reverse_lazy('admin_comment_list')
#     fields=['is_delete']
    
#     def post(self, request, *args, **kwargs):

#         comment= self.get_object()
#         print("comment", comment)
#         comment.is_delete=True
#         comment.save()
#         return super().post(request, *args, **kwargs)


from django.contrib.auth.decorators import user_passes_test
@user_passes_test(lambda u: u.is_superuser, login_url='login')

def softDeleteComment(request,pk):
    
    comment=Comment.objects.get(id=pk)
    context= { 'comments': comment}

    if request.method == 'POST':
        comment.is_delete=True
        comment.save()
        messages.success(request,'Comment deleted successfully')
        return redirect('admin_comment_list')
    
    
    return render(request,'dashboard/comments/delete_comments.html', context)


from post.models import Contact 

class ContactInfoView(SuperUserRequiredMixin, ListView):

    model=Contact 
    template_name='dashboard/contact/contact_info.html'
    paginate_by=10

    context_object_name= 'contacts'
    queryset= Contact.objects.all().order_by('date_sent')


class ContactDetailsView(SuperUserRequiredMixin,DetailView):
    
    model=Contact
    template_name= 'dashboard/contact/contact_details.html'
    context_object_name= 'contacts'

    
    def get_object(self):
        pk=self.kwargs.get('pk')
        return Contact.objects.get(pk=pk)



from post.models import Notification


class NotificationView(ListView, StaffOrSuperuserRequiredMixin):
    template_name='dashboard/users/all_notifications.html'
    model=Notification
    context_object_name='notification'

    def get_queryset(self):
          return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    


from django.http import JsonResponse
from django.template.loader import render_to_string
# for admin ko sorting 
class AjaxCategoryListView(StaffOrSuperuserRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/category/partial_category_list.html'
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        # Debugging: print all categories
        for category in self.object_list:
            print(f"Category Name: {category.name} | ID: {category.id}")
        
        # Render template with request
        html = render_to_string(
            self.template_name,
            {self.context_object_name: self.object_list},
            request=request
        )
        return JsonResponse({'html': html})

    


class AjaxAuthorListView( SuperUserRequiredMixin, ListView):
    model=User
    template_name='dashboard/users/author_partial_list.html'
    context_object_name='authors'

    def get_queryset(self):
        return self.model.objects.filter(is_staff=True)

    def get(self, request, *args, **kwargs):    
        self.object_list = self.get_queryset()
        print("Author List:")
        for author in self.object_list:
            print(f"Username: {author.username}, Email: {author.email}")
        html= render_to_string(self.template_name, {self.context_object_name: self.object_list})
        return JsonResponse({'html': html})
    
    


from django.contrib.auth import get_user_model
class AuthorPostAdminView(SuperUserRequiredMixin, ListView):
        template_name = 'dashboard/users/author_posts.html'
        queryset=User.objects.filter(is_staff=True)
        context_object_name= 'posts'
        paginate_by=10

        def get_queryset(self):
            author_pk=self.kwargs.get('pk')
            author=get_object_or_404(get_user_model(), pk=author_pk)
            return Post.objects.filter(author=author).order_by('date_posted')
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['author'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
            return context



class AuthorPostSortedView(SuperUserRequiredMixin, ListView):
    model=Post
    template_name = 'dashboard/posts/sorted_posts.html'
    context_object_name = 'posts'
    paginate_by=10

    def get_queryset(self):
        return Post.objects.all().order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context