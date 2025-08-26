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
    path ('mark-as-read/',views.MarkAllNorificationRead.as_view(), name='mark_all_read'),
    path ('notification-details/<int:pk>/redirect/',views.notificationDetailView, name='notification_details'),

    # comment related urlss
    path('edit-comment/<int:pk>/', views.EditCommentView.as_view(), name='edit_comment'),
    path('edit_comment-users/<int:pk>/', views.EditCommentUserView.as_view(), name='edit_comment_users'),
    path('delete-comment/<int:pk>/', views.DeleteCommentUserView.as_view(), name='delete_comment'),
    # path('delete-reply-comment/<int:pk>/', views.DeleteReplyCommentUserView.as_view(), name='delete_reply_comment'),
    # path('reply-comment/<int:pk>/', views.ReplyCommentView.as_view(), name='reply_comment'),
    # searching urlsss

    path('search/',views.SearchPostView.as_view(), name='search'),
    path('search_category/', views.SearchCategoryView.as_view(), name='search_category'),
    path('serach-user/', views.SearchUserView.as_view(), name='search_user'),
    path('search-comments/', views.SearchCommentsView.as_view(), name='serach_comments'),
    path('search-contact/', views.SearchContactView.as_view(), name='search_contact'),
    path('search-author/', views.SearchAuthorView.as_view(), name='search_author'),
    path('search-mypost/', views.SearchAuthorPostView.as_view(), name='search_mypost'),


    # path('delete-comments<int:pk>/', views.softDeleteCommentByUser, name='delete_comment_by_user'),


] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

