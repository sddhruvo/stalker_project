from django.urls import path
from .views import (post_comment_create_and_list_view, 
                    like_unlike_post,
                    PostDeleteView, 
                    PostUpdateView, 
                    CommentDeleteView, 
                    CommentUpdateView)

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_and_list_view, name='main_post_list'),
    path('liked/', like_unlike_post, name='like_post_list'),
    path('<uuid:id>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<uuid:id>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<uuid:id>/com-delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<uuid:id>/com-update/', CommentUpdateView.as_view(), name='comment_update'),
]