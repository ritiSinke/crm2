from django.shortcuts import render,redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from post.models import Post 
from django.views.generic import TemplateView,FormView,DeleteView 
from post.models import Post, Category, User
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


# Create your views here.


@login_required
def dashboard(request):
    admin=False

    if request.user.is_superuser or request.user.is_staff:
        admin = True
    else:
        return redirect('all-posts')
    return render(request, 'dashboard/index.html',{
        'admin': admin,
    })



class DashboardDetailsView(TemplateView):

    template_name = 'dashboard/dashboard_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.count()
        context['categories'] = Category.objects.count()
        context['users']= User.objects.count() 
        context['authors']= User.objects.filter(is_staff=True).count()
        
        return context
 


class CategoryListView(TemplateView):
    template_name = 'dashboard/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    


class UserListView(TemplateView):
    template_name = 'dashboard/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
    


class CategoryAddView(FormView):
    template_name = 'dashboard/add_category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Category added successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error adding category')
        return self.render_to_response(self.get_context_data(form=form))
    
class CategoryUpdateView(FormView):
    template_name = 'dashboard/update_category.html'
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
    
class CategoryDeleteView(DeleteView):

    model = Category
    template_name = 'dashboard/category_confirm_delete.html'  

    success_url=reverse_lazy('category_list')

    # messages.success(self.request,'User deleted successfully')
    
    

