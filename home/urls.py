from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('signup/', views.signup, name="signup"),
    path('item/', views.item, name="add_item"),
    path('item-view/', views.item_view, name="item_view"),
    path('item-view/<int:pk>/', views.PostDisplay.as_view(), name="item_details"),
    path('item-view/<int:pk>/like', views.AddLike.as_view(), name="like"),
    path('item-view/<int:pk>/dislike', views.AddDislike.as_view(), name="dislike"),
    path('item-view/<int:pk>/delete', views.DeleteItemView.as_view(), name="delete-item"),
    path('item-view/<int:pk>/edit', views.ItemEditView.as_view(), name="edit-item"),
    path('comment/<int:pk>/', views.PostComment.as_view(), name='add-comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('comment/<int:pk>/edit/', views.CommentEditView.as_view(), name='edit-comment'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
]