from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from post.models import Post 
from django.views.generic import TemplateView,FormView,DeleteView , ListView, DetailView, CreateView, UpdateView
from post.models import Post, Category, User, Comment 
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from post.views import SuperUserRequiredMixin
from accounts.views import StaffOrSuperuserRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

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
from django.http import HttpResponseForbidden

# for admin ko sorting 
class AjaxCategoryListView(UserPassesTestMixin , ListView):
    model = Category
    template_name = 'dashboard/category/partial_category_list.html'
    context_object_name = 'categories'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You are not authorised to ")
        return super().handle_no_permission()
    
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
    



from django.contrib.auth.models import Group

class GroupListView(UserPassesTestMixin, ListView):
    model=Group
    template_name='dashboard/groups/group_list.html'
    context_object_name='groups'
    queryset= Group.objects.all() 


    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You are not authorized to  see teh group of db only superuser can see that")
        return super().handle_no_permission()
    

from accounts.forms import GroupForm

class GroupAddView(UserPassesTestMixin, CreateView):

    model=Group
    template_name='dashboard/groups/add_groups.html'
    form_class=GroupForm
    success_url=reverse_lazy('group_list')

    def test_func(self):
        return self.request.user.has_perm("auth.add_group")
    
    def handle_no_permission(self):
        if self.request.user.is_autheticated:
            return HttpResponseForbidden("You are not allowded to add the group")
        return super().handle_no_permission()
    
    def form_valid(self,form):
        response = super().form_valid(form)   

        messages.success(self.request, f"Group '{form.instance.name}' created successfully!")
        return response


    def form_invalid(self, form):
        messages.error(self.request, " Failed to create group.")
        return super().form_invalid(form)
    
class GroupUpdateView(UserPassesTestMixin, UpdateView):
    
    model=Group 
    template_name="dashboard/groups/add_groups.html"
    form_class= GroupForm
    context_object_name="group"
    pk_url_kwarg = "pk"
    success_url=reverse_lazy('group_list')

    def test_func(self):
        return self.request.user.has_perm("auth.change_group")
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You are not authorized to update the group")
        return super().handle_no_permission()
    
    def form_valid(self, form):
        group= form.save(commit=False)
        group.save()

        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning("Not able to update the group ")
        response = super().form_invalid(form)
        return response 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context['groups']=self.get_object()
        return context
    
class GroupDeleteView(UserPassesTestMixin,DeleteView):
    model=Group
    template_name="dashboard/groups/delete_groups.html"
    success_url=reverse_lazy('group_list')

    def test_func(self):
        return self.request.user.has_perm("auth.delete_group")
    

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You cannot delete the group ")
        return super().handle_no_permission()
    
    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        messages.success(request, " Group '{group.name}' deleted successfully!")
        return super().delete(request, *args, **kwargs)

from accounts.models import User 

class GroupUserView(UserPassesTestMixin, ListView):
    model=Group
    template_name="dashboard/groups/group_users.html"
    context_object_name="users"

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You are not allowded to add user to group")
        return super().handle_no_permission()
    
    def get_queryset(self):
        group_id=self.kwargs['pk']
        group=Group.objects.get(pk=group_id)
        return group.user_set.all()   

    def get_group(self):
        """Return the group instance based on URL pk."""
        return get_object_or_404(Group, pk=self.kwargs['pk'])

   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.get_group()  # pass group to template
        return context


 
