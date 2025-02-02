from django.urls import path
from .views import (
    IndexView, PostView, CategoryView, ProfileView, PostCreateView,
    ProfileEditView, PostUpdateView, AddCommentView, EditCommentView,
    PostDeleteView, CommentDeleteView, send_test_email
)
app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('edit/', ProfileEditView.as_view(), name='edit_profile'),
    path(
        'category/<slug:slug>/',
        CategoryView.as_view(),
        name='category_posts'
    ),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<post_id>/', PostView.as_view(), name='post_detail'),
    path('posts/<post_id>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path(
        'posts/<post_id>/delete/',
        PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'posts/<post_id>/comment/',
        AddCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<post_id>/edit_comment/<comment_id>/',
        EditCommentView.as_view(), name='edit_comment'),
    path(
        'posts/<post_id>/delete_comment/<comment_id>/',
        CommentDeleteView.as_view(),
        name='delete_comment'),
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
    path('send-test-email/', send_test_email, name='send_test_email'),
]
