from django.urls import path
from . import views

urlpatterns = [
    path('user/',views.userPage, name="userPage"),
    path('adminPage/',views.adminPage, name="adminPage"),
    path('',views.home,name="home"),
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
]