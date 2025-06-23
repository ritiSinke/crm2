from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from . import forms as fm 
from django.contrib.auth.decorators import login_required 
from django.views.generic import CreateView
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

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
        # print("📧 Sending welcome email to:", self.object.email)

        messages.success(self.request,'Account created Succesfully')
        return super().form_valid(form)
    
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    


class LoginView(FormView):
    template_name='accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
    
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

class CreateLogoutView(LogoutView):
    next_page = reverse_lazy('login') 

    def dispatch(self, request, *args, **kwargs):

        #  logout(request) # user ko session end garxa 
         messages.success(self.request,"Logout Successfully!")
         return super().dispatch(request, *args, **kwargs)

   
    
class CustomPasswordChangeView(PasswordChangeView):
    template_name='accounts/change_password.html'
    success_url=reverse_lazy( 'login')
    form_class = fm.UserPasswordChangeForm

    def form_valid(self,form):

        self.object = form.save()

        messages.success(self.request,"Password Changed Successful")
        return super().form_valid(form)    
    