from django.urls import path 
from . import views
from dashboard.views import softDeleteComment
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[


    path('', views.all_posts, name='all-posts'),
    path ('add-post/', views.add_post, name= 'add-post'),
    path('update-post/<int:pk>/', views.update_post, name='update-post'),
    path('post-details/<int:pk>/', views.post_details, name='post-details'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),
    path('like-post/<int:pk>/', views.like_post, name='like-post'),
    path('author-post/<int:pk>/', views.author_posts, name='author-post'),
    path('search-post/',views.search_posts, name='search_posts'  ),
    path('post/<int:pk>/likes-json/', views.post_likes, name='post-likes'),
    path('my-post/', views.AuthorPostView.as_view(), name='my_post'),

    path('contact/', views.ContactView.as_view(), name='contact'),  
    path('category/<int:pk>/', views.CategoryPostsView.as_view(), name='category-posts'),
    
    path('admin-posts/',views.AdminPostView.as_view(),name='admin_post'),
    path('admin-comments-list/',views.CommentListView.as_view(), name='admin_comment_list'),
    # path('delete-comments/<int:pk>/', CommentUpdateView.as_view(),name='delete_comment'),
    

    #  admin ko features 
    path('delete_comments/<int:pk>/', softDeleteComment,name='delete_comment'),
    path('post-post-details/<int:pk>/',views.AdminPostDetailsView.as_view() , name='admin_post_details'),
    path('search/',views.SearchPostView.as_view(), name='search'),
    path ('mark-as-read/',views.MarkAllNorificationRead.as_view(), name='mark_all_read'),


] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

