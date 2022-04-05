from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('item/', views.item, name="add_item"),
    path('item-view/', views.item_view, name="item_view"),
    path('item-view/<int:pk>/', views.PostDisplay.as_view(), name="item_details"),
    path('item-view/<int:pk>/delete', views.DeleteItemView.as_view(), name="delete-item"),
    path('comment/<int:pk>/', views.PostComment.as_view(), name='add-comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
]