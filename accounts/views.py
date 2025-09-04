from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import forms as fm 
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.contrib.auth import get_user_model
from post.views import SuperUserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

Users=get_user_model()
# Create your views here.


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden

class StaffOrSuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_staff or user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden('You are not authorised to access this page')
        return super().handle_no_permission()


#register_user
# def register_user(request):
#     if request.method == 'POST':
#         form = fm.RegistrationForm(request.POST)
#         if form.is_valid():
#             var =form.save(commit=False)
#             var.username = var.email
#             var.save()
#             messages.success(request,'Account created Succesfully')
#             return redirect('login')
#         else :
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")         
#                     # messages.warning(request,'Something went wrong')
#             return redirect('register')
#     else:
#         form = fm.RegistrationForm()
#         context ={ 'form':form}
#     return render(request, 'accounts/register.html', context)        

class RegistrationCreateView(CreateView):
    template_name = 'accounts/register.html'	
    form_class = fm.RegistrationForm 
    success_url = reverse_lazy('login')

    def form_valid(self, form):
   
        self.object = form.save()

         #  Send email after registration
        send_mail(
            subject='Welcome to Our Website!',
            message=f'Hello {self.object.first_name or self.object.email},\n\nYour account has been created successfully!',
            from_email= settings.EMAIL_HOST_USER ,
            recipient_list=[self.object.email],
            fail_silently=False
        )
        # print(" Sending welcome email to:", self.object.email)

        messages.success(self.request,'Account created Succesfully')
        return super().form_valid(form)
    
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    


class LoginView(FormView):
    template_name='accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')


    def form_valid(self, form):
        user = form.get_user()

        auth_login(self.request, form.get_user())

        self.request.session['username'] = user.username

       
        if  self.request.user.is_superuser or self.request.user.is_staff:
            messages.success(self.request, "Login Successfully!")
            # print("User is staff or superuser, redirecting to dashboard")
            # Redirect to the dashboard for staff or superusers
            return HttpResponseRedirect(reverse_lazy('dashboard'))
        else:
            return HttpResponseRedirect(reverse_lazy('all-posts'))    
    def form_invalid(self, form):
     return self.render_to_response(self.get_context_data(form=form))

#login_user
# def login_user(request):
#     if request.method == 'POST':
#         username= request.POST.get('email')
#         password =request.POST.get('password')

#         user = authenticate(request, username=username, password=password)


#         if user is not None and user.is_active:
#             login(request,user)
#             return redirect('dashboard')
#         else:
#             messages.warning(request,'Invalid credentials')
#             return redirect('login')
        
#     return render (request, 'accounts/login.html')


#logout_user
# def logout_user(request):
#     logout(request)
#     messages.success(request,'Logged out successfully')
#     return redirect ('login')

#  to ket user logout from the system 


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout Successfully!")
        return redirect(reverse_lazy('login'))



class CustomPasswordChangeView(PasswordChangeView,LoginRequiredMixin):
    template_name='accounts/change_password.html'
    success_url=reverse_lazy( 'login')
    form_class = fm.UserPasswordChangeForm

    def form_valid(self,form):

        self.object = form.save()
    
        
        superuser= Users.objects.filter(is_superuser=True)
        for admin in superuser:
        
          Notification.objects.create(
        
              user=admin,
        
              message=f"Password of  '{ self.object.username}' has been changed ",
              model_name="accounts.User",
              model_id=self.object.id
        
          )
        messages.success(self.request,"Password Changed Successfully")
        return super().form_valid(form)    
    

# user ko profile update garna ko lagi
class UpdateProfileView(View, LoginRequiredMixin):

    def get(self, request):
        form = fm.UserProfileUpdateForm(instance=request.user)
        return render(request, 'accounts/update_profile.html', {'form': form})

    def post(self, request):
        form = fm.UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            
            superuser= Users.objects.filter(is_superuser=True)

            for admin in superuser:
              Notification.objects.create(
                  user=admin,
                  message=f"User '{form.instance.username}' has been updated", 
                  model="accounts.User",
                  model_id=form.instance.id 
              )

            messages.success(request, "Profile updated successfully")
            return redirect('all-posts')
        else:
            messages.error(request, "Error updating profile")
            return render(request, 'accounts/update_profile.html', {'form': form})
        


#  superuser lai matra access dinney banauney 


from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from . import forms as fm  
from django.contrib.auth import get_user_model
from post.models import Notification
class UserStatusUpdate(UpdateView, UserPassesTestMixin):
    model = get_user_model()
    template_name = 'dashboard/users/change_status.html'
    form_class = fm.UserUpdateForm
    success_url = reverse_lazy('user_list')


    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden(" You don’t have permission to create posts.")
        return super().handle_no_permission()
        

    def form_valid(self, form):

        print("form_valid called!")

        messages.success(self.request, 'User status updated successfully')
        response = super().form_valid(form)  # only save once here


        superuser= Users.objects.filter(is_superuser=True)

        for admin in superuser:
            Notification.objects.create(
                user=admin,
                message=f"User '{self.object.username}' has been updated",
                model_name="accounts.User",
                model_id=self.object.id
            )
        return response
    
   

class UserAddView(CreateView, SuperUserRequiredMixin):

    template_name='dashboard/users/user_addition.html'
    form_class=fm.AddUserForm
    model=get_user_model
    success_url=reverse_lazy('user_list')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'User added successfully')
        return super().form_valid(form)

    

   
    

class UserDeleteView(DeleteView, SuperUserRequiredMixin):

    model=get_user_model()
    template_name='dashboard/user_delete.html'
    success_url=reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'User deleted successfully')
        return redirect(self.success_url)

  

class UpdateStaffProfile(View, StaffOrSuperuserRequiredMixin):

    def get(self, request):
        form = fm.UserProfileUpdateForm(instance=request.user)
        return render(request, 'dashboard/users/update_profile.html', {'form': form})

    def post(self, request):
        form = fm.UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            
            superuser= Users.objects.filter(is_superuser=True)

            for admin in superuser:
              Notification.objects.create(
                  user=admin,
                  message=f"User '{form.instance.username}' has been updated",
                  model_name="accounts.User",
                  model_id= form.instance.id
              )

            messages.success(request, "Profile updated successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Error updating profile")
            return render(request, 'dashboard/users/update_profile.html', {'form': form})


class StaffPasswordChange(PasswordChangeView,StaffOrSuperuserRequiredMixin):

        template_name='dashboard/users/forget_password.html'
        success_url=reverse_lazy('login')
        form_class=fm.UserPasswordChangeForm

        def form_valid(self, form):
            
            self.object= form.save()

            superuser=Users.objects.filter(is_superuser=True)

            for admin in superuser:
                Notification.objects.create(
                    user=admin,
                    message=f" Password of '{ self.object.username}' has been changed ",
                    model_name="accounts.User",
                    model_id=self.object.id
                )
            return super().form_valid(form)
        



#  user ko details view garney 
class UserDetailView(DetailView, SuperUserRequiredMixin):
    model= Users
    template_name = 'dashboard/users/users_details.html'
    context_object_name = 'users'

   
from .forms import UserPermissionForm
from django.contrib.auth.models import Permission

class EditUserPermissionView(UserPassesTestMixin, UpdateView):
    model = Users
    form_class = UserPermissionForm
    template_name = 'dashboard/users/edit_user_permissions.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.request.user.is_superuser 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['permissions'].queryset = Permission.objects.all()
        form.initial['permissions'] = self.object.user_permissions.all() 
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        messages.success(self.request, f"Permissions for '{self.object.username}' updated successfully.")
        return super().form_valid(form)



from django.contrib.auth.models import Group 
from .forms import GroupPermissionForm
# Group ko permission edit

class EditGroupPermission(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Group
    template_name='dashboard/groups/edit_group_permissions.html'
    form_class=GroupPermissionForm
    pk_url_kwarg = 'group_id'
    success_url = reverse_lazy('group_list')


    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You can not chnage the permission")
        return super().handle_no_permission()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['permissions'].queryset = Permission.objects.all()
        form.initial['permissions'] = self.object.permissions.all() 
        return form
    

    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.save()
        form.save_m2m()
        messages.success(self.request, f"Permissions for '{self.object.name}' updated successfully.")
        return super().form_valid(form)        
    

class AddUserToGroupView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Group
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return HttpResponseForbidden("You cannot add users to the group.")
        return super().handle_no_permission()
    
    def get(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        users = Users.objects.exclude(groups=group)   # list of users not in this group
        return render(request, "dashboard/groups/add_users.html", {
            "group": group,
            "users": users
        })
    
    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        selected_user_ids = request.POST.getlist("users")

        for user_id in selected_user_ids:
            user = Users.objects.get(pk=user_id)
            user.groups.add(group)

        messages.success(request, f"Users added to group '{group.name}'.")
        return redirect("groups_users", pk=group_id)