from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import profile
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]