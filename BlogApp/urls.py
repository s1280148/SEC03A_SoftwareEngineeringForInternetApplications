from django.urls import path
from BlogApp import views

urlpatterns = [
    path('post/list', views.PostListView.as_view(), name="post-list"),
    path('post/search', views.PostSearchView.as_view(), name="post-search"),
    path('post/my-list', views.PostMyListView.as_view(), name="post-my-list"),
    path('post/bookmark-list', views.PostBookmarkListView.as_view(), name="post-bookmark-list"),
    path('post/<int:pk>/detail', views.PostDetailView.as_view(), name="post-detail"),
    path('post/create', views.PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name="post-delete"),
    path('post/<int:post_id>/bookmark/create', views.create_bookmark, name="post-bookmark-create"),
    path('post/<int:post_id>/bookmark/delete', views.delete_bookmark, name="post-bookmark-delete"),
    path('post/<int:post_id>/comment/create', views.create_comment, name="post-comment-create"),
    path('user/list', views.UserListView.as_view(), name="user-list"),
    path('user/signup', views.SignUpView.as_view(), name="signup"),
    path('user/login', views.BlogLoginView.as_view(), name="login"),
    path('user/logout', views.BlogLogoutView.as_view(), name="logout"),
]