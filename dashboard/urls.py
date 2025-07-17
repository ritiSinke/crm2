from django.urls import path
from . import views
from .views import CategoryDeleteView

urlpatterns =[
    path('', views.dashboard, name='dashboard'), 
    path('dashboard-details/', views.DashboardDetailsView.as_view(), name='dashboard-details'),
    path('category-list/', views.CategoryListView.as_view(), name='category_list'),
    path('user-list/',views.UserListView.as_view(),name='user_list'),
    path('category-add/', views.CategoryAddView.as_view(), name='category_add'),
    path('category-update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
    path('author-list/',views.AuthorListView.as_view(), name='author_list'),
    path('contact-list/', views.ContactInfoView.as_view(), name='contact_info'),
    path('contact-details/<int:pk>/', views.ContactDetailsView.as_view(), name='contact_details'),
    
]