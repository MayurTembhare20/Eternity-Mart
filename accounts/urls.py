from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login_View.as_view(), name="LoginView"),
    path('logout', views.logout_view, name="logout_view"),
    path('create_account', views.Register_View.as_view(), name="register_View"),
    path('profile', views.Profile_View.as_view(), name="Profile_View")
   
]