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

# Create your views here.


@login_required
@staff_member_required
def dashboard(request):
    admin=False

    if request.user.is_superuser or request.user.is_staff:
        admin = True
    else:
        return redirect('all-posts')
    

    notifications = request.user.notifications.order_by('-created_at')[:10]

    return render(request, 'dashboard/index_dashboard.html',{
        'admin': admin,
        'posts' : Post.objects.count(),
        'categories' : Category.objects.count(),
        'users' :User.objects.count(), 
        'authors' :User.objects.filter(is_staff=True).count(),
        'notifications': notifications,   

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
    


class CategoryListView(LoginRequiredMixin, TemplateView):
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

class NotificationView(ListView):
    template_name='dashboard/users/all_notifications.html'
    model=Notification
    context_object_name='notification'

    def get_queryset(self):
          return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
