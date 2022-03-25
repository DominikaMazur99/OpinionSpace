from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('item/', views.item, name="add_item"),
    path('item-view/', views.item_view, name="item_view"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
]