from django.urls import path
from . import views

urlpatterns=[
    # path('register/', views.register_user, name='register'),
    path('register/', views.RegistrationCreateView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('login/', views.login_user, name='login'),
    path ('logout/', views.logout_user, name='logout'),

]

