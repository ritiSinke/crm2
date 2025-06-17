from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path('', views.all_posts, name='all-posts'),
    path ('add-post/', views.add_post, name= 'add-post'),
    path('update-post/<int:pk>/', views.update_post, name='update-post'),
    path('post-details/<int:pk>/', views.post_details, name='post-details'),
    path('my-post/', views.my_post, name='my-post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),
    # path('like-post/<int:pk>/', views.like_post, name='like-post'),
    path('author-post/<int:pk>/', views.author_posts, name='author-post')
  
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

