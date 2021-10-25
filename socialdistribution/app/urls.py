from django.urls import include, path
from . import views

app_name = "app"
urlpatterns = [
    path('', views.index, name="index"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    path('create-post/', views.create_post, name='create-post'),
    path('posts/<str:post_id>/create-comment', views.create_comment, name='create-comment'),
    path('posts/edit-post/<str:post_id>', views.edit_post, name='edit-post'),
    path('posts/<str:post_id>', views.post, name='posts'),
    path('posts/<str:post_id>/share-post', views.share_post, name='share-post'),
    path('posts/shared/<str:shared_post_id>', views.view_shared_post, name='view-shared-post'),
    path('profile/', views.view_profile, name='view-profile'),
    path('profile/manage/', views.manage_profile, name='manage-profile'),
]
