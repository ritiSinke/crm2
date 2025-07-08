from django.urls import path
from . import views
from .forms import CreatePasswordResetForm
from django.contrib.auth.views import (
   
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
   
)
urlpatterns=[
    # path('register/', views.register_user, name='register'),
    path('register/', views.RegistrationCreateView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('login/', views.login_user, name='login'),
    path ('logout/', views.LogoutView.as_view(), name='logout'),

    path('update-profile/', views.UpdateProfileView.as_view(), name='update_profile'),

    # user ko password change garn ako lagii 
    path('change-password/', views.CustomPasswordChangeView.as_view(), name="changePassword"),

    
    path('forget-password/', PasswordResetView.as_view(template_name='accounts/forget_password.html', form_class= CreatePasswordResetForm),name='forget-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    path('user-status-update/<int:pk>/', views.UserStatusUpdate.as_view(), name='user_status_update'),
    path('user-add', views.UserAddView.as_view(),name="add_user"),
    path('user-delete/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
]   
 
