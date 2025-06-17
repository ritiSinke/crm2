from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from . import forms as fm 
from django.contrib.auth.decorators import login_required 
from django.views.generic import CreateView
from django.views.generic import FormView
from django.contrib.auth.views import LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
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
def logout_user(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect ('login')

# class CreateLogoutView(SuccessMessageMixin, LogoutView):
#     redirect_field_name = 'login'
#     next_page = reverse_lazy('login')
#     success_message = "Logged out successfully"

    
