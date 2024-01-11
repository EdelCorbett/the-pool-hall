from . import views
from django.urls import path

urlpatterns = [
    path("", views.PostList.as_view(), name="blog"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('post/<slug:slug>/comment/<int:comment_id>/edit/', views.CommentEdit.as_view(), name='comment_edit'),
    path('post/<slug:slug>/comment/<int:comment_id>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
]